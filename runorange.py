import Orange, orngAssoc
data = Orange.data.Table("TermPost.basket")

rules = Orange.associate.AssociationRulesSparseInducer(data, support=0.05, item_sets=51)
orngAssoc.sort(rules, ["support", "confidence",'lift'])
orngAssoc.printRules(rules[0:50], ["support", "confidence",'lift'])
#print "%4s %4s  %s" % ("Supp", "Conf", "Rule")
#for r in rules[:500]:
#    print "%4.1f %4.1f  %s" % (r.support, r.confidence, r)
