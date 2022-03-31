from polyglotdb import CorpusContext
import polyglotdb.io as pgio

# P1
corpus_root = '/home/michael/VMs/shared-files/polyglotDB/LibriSpeech-subset/'

parser = pgio.inspect_mfa(corpus_root)
parser.call_back = print

with CorpusContext('pg_tutorial_subset') as c:
   c.load(parser, corpus_root)

# P2
# with CorpusContext('pg_tutorial') as c:
#  print('Speakers:', c.speakers)
#  print('Discourses:', c.discourses)

#  q = c.query_lexicon(c.lexicon_phone)
#  q = q.order_by(c.lexicon_phone.label)
#  q = q.columns(c.lexicon_phone.label.column_name('phone'))
#  results = q.all()
#  print(results)

# # P3
# from polyglotdb.query.base.func import Count, Average

# with CorpusContext('pg_tutorial') as c:
#    q = c.query_graph(c.phone).group_by(c.phone.label.column_name('phone'))
#    results = q.aggregate(Count().column_name('count'), Average(c.phone.duration).column_name('average_duration'))
#    for r in results:
#       print('The phone {} had {} occurrences and an average duration of {}.'.format(r['phone'], r['count'], r['average_duration']))
