import javalang
import os

class JavaFileVisitor:
    def __init__(self,num_lines):
        self.classes = []
        self.interfaces = []
        self.methods = []
        self.imports = set()
        self.lines = num_lines

    def analyze(self, tree):
        for path, node in tree:
            if isinstance(node, javalang.tree.PackageDeclaration):
                self.package_name = node.name
            elif isinstance(node, javalang.tree.Import):
                self.imports.add(node.path)
            elif isinstance(node, javalang.tree.ClassDeclaration):
                self.classes.append({
                    'name': node.name,
                    'methods': [method.name for _, method in node.filter(javalang.tree.MethodDeclaration)]
                })
            elif isinstance(node, javalang.tree.InterfaceDeclaration):
                self.interfaces.append(node.name)

    def display_results(self):
        print(f"Package: {self.package_name}")
        print(f"Lines: {self.lines}")
        print(f"Imports: {list(self.imports)}")
        print("Classes:")
        for class_info in self.classes:
            print(f"  {class_info['name']}")
            print(f"    Methods: {', '.join(class_info['methods'])}")
        print(f"Interfaces: {', '.join(self.interfaces)}")

def analyze_java_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    num_lines=len(content.splitlines())
    tree = javalang.parse.parse(content)
    visitor = JavaFileVisitor(num_lines)
    visitor.analyze(tree)
    visitor.display_results()

def main():
    base_path = './Calculator'
    java_file_extensions = ['.java', '.gwt']  
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if any(file.endswith(ext) for ext in java_file_extensions):
                file_path = os.path.join(root, file)
                print("\n" + "="*50)
                print(f"Analyzing: {file_path}")
                analyze_java_file(file_path)

if __name__ == "__main__":
    main()
