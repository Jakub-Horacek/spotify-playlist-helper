import matplotlib.pyplot as plt
from typing import List, Tuple
import io

class ChartGenerator:
    @staticmethod
    def create_pie_chart(data: List[Tuple[str, int]], title: str) -> io.BytesIO:
        plt.figure(figsize=(8, 6))
        labels = [item[0] for item in data]
        values = [item[1] for item in data]
        
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title(title)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return buf
        
    @staticmethod
    def create_bar_chart(data: List[Tuple[str, int]], title: str) -> io.BytesIO:
        plt.figure(figsize=(10, 6))
        labels = [item[0] for item in data]
        values = [item[1] for item in data]
        
        plt.bar(range(len(labels)), values)
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        plt.title(title)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return buf
