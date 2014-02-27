# coding=utf-8
from src.util.tools import upload_dump_to_ucp_hcp

__author__ = 'jbean'

if __name__ == '__main__':
    upload_dump_to_ucp_hcp('/home/jbean/test.txt', 'https://archive.ucp.hcp.mcp.com/webdav/data/Daily%20Backups/Reviewboard/','ucpbackup', '534hawks', False)