import os
from typing import List, Tuple, Dict
import pygraphviz as pgv
import imageio
from PIL import Image, ImageDraw
from PIL import ImageFont


class Stats:
    class Step:
        def __init__(self, assigned_nodes: Dict[str, str], blank_nodes: List[str], domains: Dict[str, List[str]]):
            self.assigned_nodes = assigned_nodes
            self.blank_nodes = blank_nodes
            self.domains = domains

    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]], domain: List[str], dirname: str):
        self.nodes = nodes
        self.edges = edges
        self.domain = domain
        self.dirname = dirname
        self.gif_dirname = "gifs"
        self.steps: List[Stats.Step] = []

    def visualize(self):
        self.clean_dir()
        self.render()
        self.add_domains()
        images = []
        for i in range(len(os.listdir(self.dirname))):
            images.append(imageio.imread(f"{self.dirname}/{i}.png"))
        if not os.path.exists(self.gif_dirname):
            os.mkdir(self.gif_dirname)
        imageio.mimsave(f'{self.gif_dirname}/{self.dirname}.gif', images, duration=1)

    def clean_dir(self):
        if os.path.exists(self.dirname):
            for file in os.listdir(self.dirname):
                os.remove(f"{self.dirname}/{file}")
        else:
            os.mkdir(self.dirname)

    def add_domains(self):
        self.add_domains_to_image(f"{self.dirname}/0.png", {n: self.domain for n in self.nodes})
        for i, step in zip(range(1, len(os.listdir(self.dirname))), self.steps):
            self.add_domains_to_image(f"{self.dirname}/{i}.png", step.domains)

    def add_domains_to_image(self, filename: str, domains: Dict[str, List[str]]):
        image = Image.open(filename)
        width, height = image.size
        image_with_border = Image.new(image.mode, (width, height + 300), (255, 255, 255))
        image_with_border.paste(image, (0, 0))
        font = ImageFont.truetype("Times-Semibold.otf", 16)
        draw = ImageDraw.Draw(image_with_border)
        draw.text((10, height + 10), self.domains_text(domains), (0, 0, 0), font=font)
        image_with_border.save(filename)

    def domains_text(self, domains: Dict[str, List[str]]):
        result = ""
        for node, domain in domains.items():
            result += f"{node}: {', '.join(domain)}\n"
        return result

    def render(self):
        g = pgv.AGraph()
        for node in self.nodes:
            g.add_node(node, style='filled')
            g.get_node(node).attr["fillcolor"] = None
        for edge in self.edges:
            g.add_edge(edge[0], edge[1])
        g.layout()
        g.draw(self.dirname + "/0.png")
        for i, step in enumerate(self.steps):
            for node in self.nodes:
                if node not in step.assigned_nodes:
                    n = g.get_node(node)
                    n.attr["fillcolor"] = None
            for a_n, c in step.assigned_nodes.items():
                n = g.get_node(a_n)
                n.attr["fillcolor"] = self.get_color_name(c)
            g.draw(f"{self.dirname}/{i+1}.png")

    def get_color_name(self, color: str):
        if color == 'R':
            return "red"
        if color == 'G':
            return "green"
        if color == 'B':
            return "blue"
        raise Exception("Unknown color")
