#! /usr/bin/python3

#
# md_h_to_liq.py
# 
# Parses a markdown file from standard input and appends a list of all headers to the inner-nav variables
# of the front matter. If no front matter is defined, then it's a no-op. Output goes to standard out.
# 
# author: Bradley McFadden
# date: 2023-07-04
# 
# usage:
# md_h_to_liq.py < md_file > md_file.new
#
# cat md_file | md_h_to_liq.py > md_file.new
#

import re
import sys
import urllib.parse

HL_FENCE = "hl-fence"
END_HL_FENCE = "end-hl-fence"
HEADER = "header"
LIQUID_DEF = "liquid-def"
CODE_FENCE = "code-fence"
EMPTY = "empty"
FM_FENCE = "fm-fence"
OTHER = "other"
EOF = "eof"
ALT_H1 = "h1-alt"
ALT_H2 = "h2-alt"

class MdParser:
    def __init__(self):
        self.state = 0
        # holds last line read
        self.current_line = ""
        self.nav_labels = []
        # holds regex objects
        self.tokens = MdParser.compile_tokens()
        # finite automata
        self.fa = self.automata()
        # holds last match found
        self.last_match = None
        # holds each line of the file
        self.file_buffer = []
        # holds the token that each line represents
        self.token_buffer = []

    def parse(self, filelike=sys.stdin) -> None:
        buffer = filelike.readlines()

        for line in buffer:
            token, self.last_match = self.match_line_to_token(line)
            self.current_line = line

            if self.last_match:
                self.fa[self.state][token]()

            self.file_buffer.append(line)
            self.token_buffer.append(token)


    def output(self, filelike=sys.stdout) -> None:
        wrote_inner_nav = False
        fm_fence_count = 0

        for token, line in zip(self.token_buffer, self.file_buffer):
            if not wrote_inner_nav:
                if token == LIQUID_DEF:
                    match = self.tokens[LIQUID_DEF].match(line)
                    var_name = match.group(1)
                    if var_name == "inner-nav":
                        filelike.write("inner-nav: {}\n".format(self.encoded_inner_nav()))
                        wrote_inner_nav = True
                    else:
                        filelike.write(line)
                elif token == FM_FENCE:
                    fm_fence_count += 1
                    if fm_fence_count == 2:
                        filelike.write("inner-nav: {}\n".format(self.encoded_inner_nav()))
                        wrote_inner_nav = True
                    filelike.write(line)
                else:
                    filelike.write(line)
            else:
                filelike.write(line)

    def encoded_inner_nav(self) -> str:
        return ",".join([urllib.parse.quote(label, safe='') for label in self.nav_labels])

    def match_line_to_token(self, line): # (token, match)
        for k, v in self.tokens.items():
            match = v.match(line)
            if match:
                return (k, match)
        # endfor

        return (OTHER, None)

    def compile_tokens() -> dict:
        return {
            HL_FENCE : re.compile(r"^\s*{%\s*highlight\s+(\S+)\s*%}\s*$"),
            END_HL_FENCE : re.compile(r"^\s*{%\s*endhighlight\s*%}\s*$"),
            HEADER : re.compile(r"^#+\s+(.*)\s*$"),
            LIQUID_DEF : re.compile(r"^([a-zA-Z0-9_-]+):\s*(.*)\s*$"),
            CODE_FENCE : re.compile(r"^\s*```\s*.*\s*$"),
            FM_FENCE : re.compile(r"^---\s*$"),
            EMPTY : re.compile(r'^\s*$'),
            ALT_H1 : re.compile(r'^=+\s*$'),
            ALT_H2 : re.compile(r'^-+\s*$'),
        }

    def automata(self) -> dict:
        return {
            # initial state; possible exit
            0 : {
                FM_FENCE : lambda : self.set_state(1),
                HL_FENCE: self.reject,
                END_HL_FENCE : self.reject,
                HEADER : self.reject,
                LIQUID_DEF : self.reject,
                CODE_FENCE : self.reject,
                EOF : self.accept,
                EMPTY : self.nop,
                OTHER: self.nop,
                ALT_H1 : self.reject,
                ALT_H2 : self.reject,
            },
            # parsed one front matter fence
            1 : {
                FM_FENCE: lambda : self.set_state(2),
                HL_FENCE: self.reject,
                END_HL_FENCE : self.reject,
                HEADER : self.reject,
                LIQUID_DEF : self.line_to_liquid_def,
                CODE_FENCE : self.reject,
                EOF : self.reject,
                EMPTY : self.nop,
                OTHER : self.nop,
                ALT_H1 : self.reject,
                ALT_H2 : self.reject,
            },
            # parsed two front matter fences; possible exit
            2 : {
                FM_FENCE: self.reject,
                HL_FENCE: lambda : self.set_state(4),
                END_HL_FENCE : self.reject,
                HEADER : self.line_to_inner_nav,
                LIQUID_DEF : self.reject,
                CODE_FENCE : lambda : self.set_state(3),
                EOF: self.accept,
                EMPTY : self.nop,
                OTHER: self.nop,
                ALT_H1 : self.prev_line_to_inner_nav,
                ALT_H2 : self.prev_line_to_inner_nav,
            },
            # parsed one code fence
            3 : {
                CODE_FENCE : lambda : self.set_state(2),
                EOF : self.reject,
                EMPTY : self.nop,
                OTHER : self.nop,
                ALT_H1 : self.reject,
                ALT_H2 : self.reject,
            },
            # parsed highlight fence
            4 : {
                END_HL_FENCE : lambda : self.set_state(2),
                EOF : self.reject,
                EMPTY : self.nop,
                OTHER : self.nop,
                ALT_H1 : self.reject,
                ALT_H2 : self.reject,
            }
        }

    def nop(self) -> None:
        pass

    def reject(self) -> None:
        pass

    def accept(self) -> None:
        pass

    def set_state(self, new_state: int) -> None:
        self.state = new_state

    def line_to_inner_nav(self) -> None:
        tokens = self.current_line.lower().strip().split(" ")
        # print(tokens)
        nav_label = "-".join([x.lower() for x in tokens[1:]])
        self.append_to_nav_labels_uniq(nav_label)

    def prev_line_to_inner_nav(self) -> None:
        if self.last_token != EMPTY:
            tokens = self.last_line().lower().strip().split(" ")
            nav_label = "-".join(tokens)
            self.append_to_nav_labels_uniq(nav_label)

    def line_to_liquid_def(self) -> None:
        pass
        # var_name = self.last_match.group(1)
        # var_value = self.last_match.group(2)
        # 
        # if var_name == "inner-nav":
        #     self.extend_to_nav_labels_uniq(var_value.split(","))

    def last_line(self) -> str:
        return self.file_buffer[-1:][0]

    def last_token(self) -> str:
        return self.token_buffer[-1:][0]
    
    def extend_to_nav_labels_uniq(self, labels: list) -> None:
        for label in labels:
            self.append_to_nav_labels_uniq(label)

    def append_to_nav_labels_uniq(self, label: str) -> None:
        if not label in self.nav_labels:
            self.nav_labels.append(label)


def main() -> None:
    parser = MdParser()
    parser.parse()
    parser.output()


if __name__ == "__main__":
    main()
