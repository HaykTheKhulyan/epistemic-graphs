#!/usr/bin/env python3
from graphviz import Digraph
import json
import queue

class EG:
    green='forestgreen'
    red='firebrick3'

    def __init__(self, name, format_str, dark=False, json_file_name=None):
        self.arg_name = 'A'
        self.dark = dark
        self.format_str = format_str

        # neato could be useful for heavier graphs
        self.graph = Digraph(name, filename=name, format=format_str, engine='dot')
        self.graph.attr(ratio='0.2') # for dot
        #self.graph.attr(overlap='false', sep='+1') # for neato
        self.graph.attr(rankdir='BT')
        if self.format_str != 'svg':
            self.graph.attr(dpi='300')

        self.graph.attr('node', shape='box', style='rounded')

        if dark:
            self.graph.attr(bgcolor='gray15', fontcolor='white')
            self.graph.attr('node', fontcolor='white')

        if (not json_file_name == None):
            # data object that will store the json data for the belief
            data = []

            # opens the json and loads the info into data
            with open("belief_data/" + json_file_name) as json_file:
                data = json.load(json_file)

            # adds the primary node to the graph
            primary = self.node('none', data["arg_str"], [], primary=True)
            # calls the link_graph method which adds the rest of the nodes
            self.link_graph_depth(data["children"], primary)

            # this chunk was for the breadth that i was testing
            # node_queue = queue.SimpleQueue()
            # for child in data["children"]:
            #     node_queue.put(child)
            # self.link_graph_depth(node_queue, data)

            # calls the finish method and sets the title to the claim
            self.finish(f'\nArguments For & Against:\n{data["arg_str"]}')

    # this one names nodes in a depth first approach
    def link_graph_depth(self, nodes_to_add, parent_node):
        # base case
        if (len(nodes_to_add) == 0):
            return
        else:
            for node in nodes_to_add:
                new_node = self.node(node["side"], node["arg_str"], parent_node)

                self.link_graph_depth(node["children"], new_node)


    # breadth doesn't work, can't figure it out.
    # this one names nodes in a breadth first approach (the way blunaxela originally made it)
    # add nodes to a queue, then process each one?
    # def link_graph_breadth(self, nodes_to_add, parent_node):
    #     # base case
    #     if (len(nodes_to_add) == 0):
    #         return
    #     else:
    #         node_queue = queue.SimpleQueue()
    #         for node in nodes_to_add:
    #             new_node = self.node(node["side"], node["arg_str"], parent_node)
    #             node_queue.put(node)
    #
    #         while(not node_queue.empty()):
    #             self.link_graph_breadth(node["children"], new_node)
    #             node_queue.get()

    # def link_graph_breadth(self, node_queue, primary_node):
    #     previous_node = primary_node
    #     print("prev node")
    #     print(previous_node)
    #
    #     while(not node_queue.empty()):
    #         current_node = node_queue.get()
    #         print("this is the current node:")
    #         print(current_node["arg_str"])
    #
    #         for child in current_node["children"]:
    #             node_queue.put(child)
    #
    #         self.node(current_node["side"], current_node["arg_str"], previous_node)
    #         previous_node = current_node
    #
    #
    #         # while(not node_queue.empty()):
    #         #     print(node_queue.get()["arg_str"])
    #         #     print("XXXXXXXXXXXXXXXXXXXXXXXXX")






    def incr_chr(self, c):
        return chr(ord(c) + 1) if c != 'Z' else 'A'

    def incr_str(self, s):
        lpart = s.rstrip('Z')
        num_replacements = len(s) - len(lpart)
        new_s = lpart[:-1] + self.incr_chr(lpart[-1]) if lpart else 'A'
        new_s += 'A' * num_replacements
        return new_s

    def link(self, side, A, B):
        arg_color = 'white' if self.dark else 'black'
        if side == 'for':
            arg_color = EG.green
        elif side == 'against':
            arg_color = EG.red

        self.graph.edge(A, B, color=arg_color)

    def node(self, side, arg_str, conns, primary=False, url=''):
        arg_color = 'white' if self.dark else 'black'
        if side == 'for':
            arg_color = EG.green
        elif side == 'against':
            arg_color = EG.red

        rank = 'source' if primary else 'sink'
        if self.format_str == 'svg' and url != '':
            self.graph.node(self.arg_name, f'{self.arg_name} = {arg_str}\n(click for link)', color=arg_color, rank=rank, URL=url)
        else:
            if url != '':
                self.graph.node(self.arg_name, f'{self.arg_name} = {arg_str}\n(see footnotes)', color=arg_color, rank=rank)
                print(f'{self.arg_name}: {url}')
            else:
                self.graph.node(self.arg_name, f'{self.arg_name} = {arg_str}', color=arg_color, rank=rank)

        for c in conns:
            self.graph.edge(self.arg_name, c, color=arg_color)

        return_name = self.arg_name
        self.arg_name = self.incr_str(self.arg_name)
        return return_name

    def finish(self, title_str):
        self.graph.attr(label=title_str)

        #f.view()
        self.graph.render()
