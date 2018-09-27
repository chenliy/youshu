# -*- coding: utf-8 -*-
from IKEA.cpws.config import ws_type_article
from IKEA.cpws.config import case_keys
from IKEA.cpws.config import court_reg
import re

def find_paragraph(keys, articles):
    paragraphs = list(set([a for a in articles for k in keys if k in a]))
    paragraph_indexs = sorted([articles.index(p) for p in paragraphs])
    return paragraph_indexs


def verdict_extract(verdicts):
    _verdict = '<br>'.join(verdicts)
    verdict_indexs = sorted([_verdict.find(key) for key in ['未按本判决指定', '受理费']])
    verdict_indexs = [v for v in verdict_indexs if v != -1]
    verdict = _verdict[:verdict_indexs[0]] if verdict_indexs else _verdict
    symbol_indexs = sorted([verdict.rfind(key) for key in ['，', '。']])
    symbol_indexs = [v for v in symbol_indexs if v != -1]
    verdict = verdict[:symbol_indexs[-1]+1] if symbol_indexs else verdict
    return verdict

def paragraph_only(articles):
    article = ' '.join(articles)
    article = re.sub('(\d) ', '\\1', article)
    article = re.sub('([\u4e00-\u9fa5]) ', '\\1', article)
    return article.split(' ')


class WenshuBase:
    """Structured caipanwenshu article
    Args
        article  caipanwenshu text content
    Return
        role_paragraph
        reason_paragraph
        verdict_paragraph
        court_paragraph
        reason_description
    """
    def __init__(self, article):
        """
        Param
            articles: list
            article: str, split by \n
            reason_paragraph: str
            verdict_paragraph: str, use for content_type
            verdict: str

        """
        self.article = article
        self.articles = self.article.split('\n')
        reason_paragraph_index = self.get_reason_paragraph_index()
        verdict_paragraph_index = self.get_verdict_paragraph_index()
        court_paragraph_index = self.get_court_paragraph_index()
        self.reason_paragraph = self.articles[reason_paragraph_index]
        self.verdict_paragraph = self.articles[verdict_paragraph_index]
        self._articles = self.articles[:reason_paragraph_index] + paragraph_only(self.articles[reason_paragraph_index:court_paragraph_index]) + self.articles[court_paragraph_index:]
        self.verdict = verdict_extract(self.articles[verdict_paragraph_index+1:court_paragraph_index])
        self.role_paragraph = self.articles[:reason_paragraph_index]
        self.court_paragraph = self.articles[court_paragraph_index:]
        reason_sentence_index = self.reason_paragraph.find('。')
        self.reason_description = self.reason_paragraph[:reason_sentence_index] if reason_sentence_index != -1 else self.reason_paragraph
        self.claims_paragraphs = self.articles[reason_paragraph_index+1: reason_paragraph_index+3]

    def get_reason_paragraph_index(self):
        # 匹配案由所在的段落,并且构造案由词典
        reason_paragraph_indexs = find_paragraph(case_keys, self.articles)
        reason_paragraph_index = reason_paragraph_indexs[0] if reason_paragraph_indexs else len(self.articles)-1
        return reason_paragraph_index

    def get_verdict_paragraph_index(self):
        # 匹配可能出现判决结果所在的段落,进一步提取判决结果和文书类型
        verdict_paragraph_indexs = find_paragraph(ws_type_article.keys(), self.articles)
        verdict_paragraph_index = verdict_paragraph_indexs[-1] if verdict_paragraph_indexs else 0
        return verdict_paragraph_index

    def get_court_paragraph_index(self):
        """采集法院人员信息"""
        regNo = court_reg()
        s = []
        for items in re.findall(regNo, self.article, re.M):
            sentence = items[0]
            s = s + [self.articles.index(t) for t in self.articles if sentence in t]
        s = sorted(list(set(s)))
        if s:
            return s[0]
        else:
            return -1

