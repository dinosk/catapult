# Copyright (c) 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
import json
import os
import tempfile
import urllib
import urllib2

from perf_insights import corpus_driver
from perf_insights import perf_insights_trace_handle
from perf_insights.value import run_info as run_info_module


_DEFAULT_PERF_INSIGHTS_SERVER = 'http://performance-insights.appspot.com'

class PerfInsightsCorpusDriver(corpus_driver.CorpusDriver):
  def __init__(self, args):
    self.directory = os.path.abspath(os.path.expanduser(args.cache_directory))
    self.server = args.server
    if not self.server:
      self.server = _DEFAULT_PERF_INSIGHTS_SERVER

  @staticmethod
  def CheckArguments(parser, args):
    if not os.path.exists(args.cache_directory):
      parser.error('trace directory does not exist')

  @staticmethod
  def AddArguments(parser):
    parser.add_argument(
        '--cache_directory',
        help='Local directory to cache traces.')
    parser.add_argument(
        '--server',
        help='Server address of perf insights.',
        default=_DEFAULT_PERF_INSIGHTS_SERVER)

  def GetTraceHandlesMatchingQuery(self, query):
    trace_handles = []

    query_string = urllib.quote_plus(query.AsQueryString())
    response = urllib2.urlopen(
        '%s/query?q=%s' % (self.server, query_string))
    file_urls = json.loads(response.read())

    for file_url in file_urls:
      run_info = run_info_module.RunInfo(
          url=file_url,
          display_name=file_url,
          run_id=file_url)

      th = perf_insights_trace_handle.PerfInsightsTraceHandle(
          run_info, self.directory)
      trace_handles.append(th)

    return trace_handles
