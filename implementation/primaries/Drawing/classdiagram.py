
from pycana import CodeAnalyzer
import classes

analyzer= CodeAnalyzer(classes)
relations= analyzer.analyze()
analyzer.draw_relations(relations, 'class_diagram.png')
