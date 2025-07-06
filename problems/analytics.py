#!/usr/bin/env python3
"""
Analytics script for Belarus Physics Olympiad Problem Bank
Analyzes problem metadata to provide insights about tags, methods, skills, and trends.
"""

import json
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import argparse
import sys

class ProblemAnalytics:
    def __init__(self, json_file='pdf_metadata.json'):
        """Initialize the analytics with problem data."""
        self.json_file = json_file
        self.problems = []
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load problem data from JSON file."""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.problems = json.load(f)
            print(f"✅ Loaded {len(self.problems)} problems from {self.json_file}")
            self.create_dataframe()
        except FileNotFoundError:
            print(f"❌ Error: {self.json_file} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            sys.exit(1)
    
    def create_dataframe(self):
        """Create pandas DataFrame from problem data."""
        # Flatten the data for easier analysis
        flat_data = []
        for problem in self.problems:
            flat_data.append({
                'id': problem['id'],
                'year': problem['year'],
                'stage': problem['stage'],
                'grade': problem['grade'],
                'number': problem['number'],
                'title': problem['title'],
                'difficulty': problem['difficulty'],
                'target': problem['target'],
                'tags_count': len(problem['tags']),
                'skills_count': len(problem['skills']),
                'methods_count': len(problem['methods']),
                'tags': problem['tags'],
                'skills': problem['skills'],
                'methods': problem['methods']
            })
        
        self.df = pd.DataFrame(flat_data)
        print(f"📊 Created DataFrame with {len(self.df)} rows and {len(self.df.columns)} columns")
    
    def get_basic_stats(self):
        """Get basic statistics about the problems."""
        print("\n" + "="*50)
        print("📈 ОСНОВНАЯ СТАТИСТИКА")
        print("="*50)
        
        print(f"📚 Всего задач: {len(self.problems)}")
        print(f"📅 Годы: {self.df['year'].min()} - {self.df['year'].max()}")
        print(f"🎓 Классы: {sorted(self.df['grade'].unique())}")
        print(f"🏆 Этапы: {sorted(self.df['stage'].unique())}")
        print(f"⚡ Уровни сложности: {sorted(self.df['difficulty'].unique())}")
        
        # Year distribution
        print(f"\n📊 Распределение по годам:")
        year_counts = self.df['year'].value_counts().sort_index()
        for year, count in year_counts.items():
            print(f"  {year}: {count} задач")
        
        # Grade distribution  
        print(f"\n🎓 Распределение по классам:")
        grade_counts = self.df['grade'].value_counts().sort_index()
        for grade, count in grade_counts.items():
            print(f"  {grade} класс: {count} задач")
            
        # Difficulty distribution
        print(f"\n⚡ Распределение по сложности:")
        difficulty_counts = self.df['difficulty'].value_counts()
        difficulty_labels = {
            'basic': 'Базовый',
            'intermediate': 'Средний', 
            'advanced': 'Продвинутый',
            'very_advanced': 'Очень сложный',
            'mixed': 'Смешанный'
        }
        for difficulty, count in difficulty_counts.items():
            label = difficulty_labels.get(difficulty, difficulty)
            print(f"  {label}: {count} задач")
    
    def analyze_tags(self, top_n=20):
        """Analyze the most frequent tags."""
        print("\n" + "="*50)
        print("🏷️  АНАЛИЗ ТЕГОВ")
        print("="*50)
        
        # Count all tags
        all_tags = []
        for problem in self.problems:
            all_tags.extend(problem['tags'])
        
        tag_counts = Counter(all_tags)
        print(f"📊 Всего уникальных тегов: {len(tag_counts)}")
        print(f"🔥 Топ-{top_n} самых популярных тегов:")
        
        for i, (tag, count) in enumerate(tag_counts.most_common(top_n), 1):
            percentage = (count / len(self.problems)) * 100
            print(f"  {i:2d}. {tag:<30} {count:3d} ({percentage:.1f}%)")
        
        return tag_counts
    
    def analyze_skills(self, top_n=15):
        """Analyze the most frequent skills."""
        print("\n" + "="*50)
        print("🎯 АНАЛИЗ НАВЫКОВ")
        print("="*50)
        
        # Count all skills
        all_skills = []
        for problem in self.problems:
            all_skills.extend(problem['skills'])
        
        skill_counts = Counter(all_skills)
        print(f"📊 Всего уникальных навыков: {len(skill_counts)}")
        print(f"🔥 Топ-{top_n} самых важных навыков:")
        
        for i, (skill, count) in enumerate(skill_counts.most_common(top_n), 1):
            percentage = (count / len(self.problems)) * 100
            print(f"  {i:2d}. {skill:<50} {count:3d} ({percentage:.1f}%)")
        
        return skill_counts
    
    def analyze_methods(self, top_n=15):
        """Analyze the most frequent methods."""
        print("\n" + "="*50)
        print("⚙️  АНАЛИЗ МЕТОДОВ")
        print("="*50)
        
        # Count all methods
        all_methods = []
        for problem in self.problems:
            all_methods.extend(problem['methods'])
        
        method_counts = Counter(all_methods)
        print(f"📊 Всего уникальных методов: {len(method_counts)}")
        print(f"🔥 Топ-{top_n} самых используемых методов:")
        
        for i, (method, count) in enumerate(method_counts.most_common(top_n), 1):
            percentage = (count / len(self.problems)) * 100
            print(f"  {i:2d}. {method:<50} {count:3d} ({percentage:.1f}%)")
        
        return method_counts
    
    def analyze_by_difficulty(self):
        """Analyze problems by difficulty level."""
        print("\n" + "="*50)
        print("📊 АНАЛИЗ ПО СЛОЖНОСТИ")
        print("="*50)
        
        for difficulty in sorted(self.df['difficulty'].unique()):
            difficulty_problems = [p for p in self.problems if p['difficulty'] == difficulty]
            
            difficulty_labels = {
                'basic': 'Базовый',
                'intermediate': 'Средний',
                'advanced': 'Продвинутый', 
                'very_advanced': 'Очень сложный',
                'mixed': 'Смешанный'
            }
            
            label = difficulty_labels.get(difficulty, difficulty)
            print(f"\n🎯 {label.upper()} ({len(difficulty_problems)} задач)")
            
            # Most common tags for this difficulty
            tags = []
            for problem in difficulty_problems:
                tags.extend(problem['tags'])
            
            tag_counts = Counter(tags)
            print(f"  Популярные теги:")
            for tag, count in tag_counts.most_common(5):
                print(f"    • {tag} ({count})")
    
    def analyze_trends(self):
        """Analyze trends over years."""
        print("\n" + "="*50)
        print("📈 АНАЛИЗ ТРЕНДОВ")
        print("="*50)
        
        # Problems per year
        year_stats = defaultdict(lambda: {'total': 0, 'grades': defaultdict(int), 'difficulties': defaultdict(int)})
        
        for problem in self.problems:
            year = problem['year']
            year_stats[year]['total'] += 1
            year_stats[year]['grades'][problem['grade']] += 1
            year_stats[year]['difficulties'][problem['difficulty']] += 1
        
        print("📊 Статистика по годам:")
        for year in sorted(year_stats.keys(), reverse=True):
            stats = year_stats[year]
            print(f"\n  {year}: {stats['total']} задач")
            
            # Grade distribution
            grades = sorted(stats['grades'].items())
            grade_str = ", ".join([f"{g} кл: {c}" for g, c in grades])
            print(f"    Классы: {grade_str}")
            
            # Most common difficulty
            top_difficulty = max(stats['difficulties'].items(), key=lambda x: x[1])
            print(f"    Основная сложность: {top_difficulty[0]} ({top_difficulty[1]} задач)")
    
    def get_recommendations(self):
        """Get recommendations for website optimization."""
        print("\n" + "="*50)
        print("💡 РЕКОМЕНДАЦИИ ДЛЯ САЙТА")
        print("="*50)
        
        # Analyze tag distribution
        all_tags = []
        for problem in self.problems:
            all_tags.extend(problem['tags'])
        tag_counts = Counter(all_tags)
        
        print("🎯 Приоритетные теги для фильтрации:")
        priority_tags = tag_counts.most_common(15)
        for i, (tag, count) in enumerate(priority_tags, 1):
            print(f"  {i:2d}. {tag}")
        
        print("\n🔍 Рекомендации по поиску:")
        print("  • Индексировать по тегам:", ', '.join([tag for tag, _ in priority_tags[:10]]))
        print("  • Добавить автодополнение для популярных тегов")
        print("  • Создать быстрые фильтры для топ-5 тегов")
        
        # Difficulty balance
        difficulty_dist = self.df['difficulty'].value_counts()
        print(f"\n⚖️  Баланс сложности:")
        print(f"  • Базовых: {difficulty_dist.get('basic', 0)}")
        print(f"  • Средних: {difficulty_dist.get('intermediate', 0)}")
        print(f"  • Продвинутых: {difficulty_dist.get('advanced', 0)}")
        print(f"  • Очень сложных: {difficulty_dist.get('very_advanced', 0)}")
        
        # Recommendations
        print(f"\n📚 Рекомендации по контенту:")
        if difficulty_dist.get('basic', 0) < 10:
            print("  • Добавить больше базовых задач для начинающих")
        if difficulty_dist.get('very_advanced', 0) > 20:
            print("  • Создать раздел для экспертов")
        
        # Year coverage
        year_range = self.df['year'].max() - self.df['year'].min()
        print(f"\n📅 Временное покрытие: {year_range + 1} лет")
        if year_range > 10:
            print("  • Добавить фильтр по десятилетиям")
            print("  • Создать раздел 'Классические задачи'")
    
    def export_data(self, format='json'):
        """Export analyzed data."""
        print("\n" + "="*50)
        print("💾 ЭКСПОРТ ДАННЫХ")
        print("="*50)
        
        # Get all analytics data
        all_tags = []
        all_skills = []
        all_methods = []
        
        for problem in self.problems:
            all_tags.extend(problem['tags'])
            all_skills.extend(problem['skills'])
            all_methods.extend(problem['methods'])
        
        analytics_data = {
            'summary': {
                'total_problems': len(self.problems),
                'years_covered': list(sorted(self.df['year'].unique())),
                'grades': list(sorted(self.df['grade'].unique())),
                'stages': list(sorted(self.df['stage'].unique())),
                'difficulties': list(sorted(self.df['difficulty'].unique()))
            },
            'tags': {
                'total_unique': len(set(all_tags)),
                'most_common': dict(Counter(all_tags).most_common(20))
            },
            'skills': {
                'total_unique': len(set(all_skills)),
                'most_common': dict(Counter(all_skills).most_common(15))
            },
            'methods': {
                'total_unique': len(set(all_methods)),
                'most_common': dict(Counter(all_methods).most_common(15))
            },
            'distributions': {
                'by_year': dict(self.df['year'].value_counts().sort_index()),
                'by_grade': dict(self.df['grade'].value_counts().sort_index()),
                'by_difficulty': dict(self.df['difficulty'].value_counts())
            }
        }
        
        # Export to JSON
        if format in ['json', 'all']:
            with open('analytics_report.json', 'w', encoding='utf-8') as f:
                json.dump(analytics_data, f, ensure_ascii=False, indent=2)
            print("📄 Exported to analytics_report.json")
        
        # Export to CSV
        if format in ['csv', 'all']:
            self.df.to_csv('problems_data.csv', index=False, encoding='utf-8')
            print("📊 Exported to problems_data.csv")
        
        return analytics_data
    
    def run_full_analysis(self):
        """Run complete analysis."""
        print("🚀 ЗАПУСК ПОЛНОГО АНАЛИЗА БАНКА ЗАДАЧ BelPhO")
        print("="*60)
        
        self.get_basic_stats()
        tag_counts = self.analyze_tags()
        skill_counts = self.analyze_skills()
        method_counts = self.analyze_methods()
        self.analyze_by_difficulty()
        self.analyze_trends()
        self.get_recommendations()
        
        # Export data
        analytics_data = self.export_data('all')
        
        print("\n" + "="*60)
        print("✅ АНАЛИЗ ЗАВЕРШЕН")
        print("="*60)
        print("📊 Создан полный отчет для оптимизации сайта")
        print("💡 Используйте рекомендации для улучшения пользовательского опыта")
        
        return analytics_data

def main():
    """Main function to run analytics."""
    parser = argparse.ArgumentParser(description='Analyze Belarus Physics Olympiad problems')
    parser.add_argument('--file', '-f', default='pdf_metadata.json', 
                       help='Path to JSON file with problem metadata')
    parser.add_argument('--export', '-e', choices=['json', 'csv', 'all'], 
                       default='all', help='Export format')
    parser.add_argument('--tags', '-t', type=int, default=20,
                       help='Number of top tags to show')
    parser.add_argument('--skills', '-s', type=int, default=15,
                       help='Number of top skills to show')
    parser.add_argument('--methods', '-m', type=int, default=15,
                       help='Number of top methods to show')
    
    args = parser.parse_args()
    
    # Run analysis
    analytics = ProblemAnalytics(args.file)
    analytics.run_full_analysis()

if __name__ == "__main__":
    main() 