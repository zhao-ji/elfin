# coding: utf-8

import logging

from pyquery import PyQuery as pq

from socrates.set import log

def timeline(content):
    open_line_init = pq(content)
    open_line_init('span').remove()
    open_line_li_list = open_line_init('li')

    single_message = lambda talk: talk[0] + '\n\n'
    normal_message = lambda talk: talk[0] + ' : ' + \
                                talk[1] + '\n\n'
    at_message = lambda talk: talk[0] + '@' + \
                                talk[1] + ' : ' + \
                                talk[2] + '\n\n'
    rt_message = lambda talk: talk[0] + ':' + \
                                talk[3] + ' ' + \
                                talk[1] + ' ' + \
                                talk[2] + ':' + ' '

    talk_func = {
        1: single_message, 2: normal_message,
        3: at_message, 4: rt_message,
        }

    open_talk_list = [list(li.itertext()) for li in open_line_li_list]
    open_talk_list = [filter(lambda i: i != ' @', talk) for talk in open_talk_list]
    open_talk_list = filter(lambda talk: not (len(talk)==4 and talk[3].strip()==unichr(int('ff01', 16))), open_talk_list)
    open_talk_list = map(lambda talk: talk_func[len(talk)](talk), open_talk_list)
    open_line = ''.join([talk.encode('utf-8') for talk in open_talk_list])
    logging.info(open_line)
    return open_line

