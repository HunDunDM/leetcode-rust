#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2019 HunDunDM. All Rights Reserved
#
"""

根据输入参数从leetcode上抓取对应题目数据并生成模板
接口参考了https://github.com/aylei/leetcode-rust/blob/master/src/main.rs

@file: new.py
@Authors: HunDunDM (hundundm@gmail.com)
@Date: 2019-03-07
"""

import os
import sys
import json

import requests
from bs4 import BeautifulSoup

TEMPLATE_FILE = './template.rs'
PROBLEMS_URL = 'https://leetcode.com/api/problems/algorithms/'
GRAPHQL_URL = 'https://leetcode.com/graphql'
QUESTION_QUERY_OPERATION = 'questionData'
QUESTION_QUERY_STRING = '''
query questionData($titleSlug: String!) {
    question(titleSlug: $titleSlug) {
        content
        stats
        codeDefinition
        sampleTestCase
        metaData
    }
}'''
MAP_DIFFICULTY = {
    1: 'Easy',
    2: 'Medium',
    3: 'Hard',
}


def difficulty_str(problem):
    level = problem['difficulty']['level']
    return MAP_DIFFICULTY[level] if level in MAP_DIFFICULTY else 'Unknown'


class Problem:
    def __init__(self, problem, detail):
        self.title = problem['stat']['question__title']
        self.title_slug = problem['stat']['question__title_slug']
        self.code_definition = json.loads(detail['data']['question']['codeDefinition'])
        self.content = detail['data']['question']['content']
        self.sample_test_case = detail['data']['question']['sampleTestCase']
        self.difficulty = difficulty_str(problem)


def new_query(client, title_slug):
    # 在aylei的rust版本中，所用的reqwest模块似乎不用处理csrf等header，有机会研究下
    query = {
        'operationName': QUESTION_QUERY_OPERATION,
        'variables': {'titleSlug': title_slug},
        'query': QUESTION_QUERY_STRING,
    }
    headers = {
        'x-csrftoken': client.cookies['csrftoken'],
        'referer': '',
    }
    response = client.post(GRAPHQL_URL, json=query, headers=headers)
    return json.loads(response.text)


def get_problem(pid):
    client = requests.session()
    problems = json.loads(client.get(PROBLEMS_URL).text)
    for problem in problems['stat_status_pairs']:
        if problem['stat']['question_id'] == pid:
            detail = new_query(client, problem['stat']['question__title_slug'])
            return Problem(problem, detail)


def get_pid():
    assert len(sys.argv) == 2, 'problem id must be provided'
    pid = sys.argv[1]
    assert pid.isdigit(), f"argv '{pid}' is not a number"
    return int(pid)


def get_desc(problem):
    return (BeautifulSoup(problem.content, features='html.parser')
            .get_text()
            .replace('\n\n', '\n')
            .replace('\n', '\n * ')
            )


def parse_extra_use(code):
    return ''


def new_code_file(pid, problem):
    assert problem is not None, f'problem #{pid} not found'
    # 提取rust默认代码
    rust_code = [detail for detail in problem.code_definition if detail['value'] == 'rust']
    assert len(rust_code) == 1, f'problem #{pid} has no rust support yet'
    rust_code = rust_code[0]['defaultCode']
    # 判断文件是否已经存在
    file_name = 'p{:04d}_{}'.format(pid, problem.title_slug).replace('-', '_')
    file_path = f'./src/{file_name}.rs'
    assert not os.path.exists(file_path), f'problem #{pid} already initialized'
    # 按模板生成代码
    with open(TEMPLATE_FILE, 'r') as fin:
        template = fin.read()
    assert template is not None, 'can not open template file'
    code = (template
            .replace('__PROBLEM_TITLE__', problem.title)
            .replace('__PROBLEM_DESC__', get_desc(problem))
            .replace('__PROBLEM_DEFAULT_CODE__', rust_code)
            .replace('__PROBLEM_ID__', str(pid))
            .replace('__EXTRA_USE__', parse_extra_use(rust_code))
            )
    with open(file_path, 'w') as fout:
        fout.write(code)
    # 其他需要追加的文件
    os.system(f"echo 'mod {file_name};' >> ./src/lib.rs")
    os.system(f"echo '* [{pid} - {problem.title}]({file_path})' >> ./README.md")
    os.system(f'git add {file_path}')


def main():
    pid = get_pid()
    problem = get_problem(pid)
    new_code_file(pid, problem)


if __name__ == '__main__':
    main()
