import orange, orngAssoc
data = orange.ExampleTable("TermPostTable.csv")
data = orange.Preprocessor_discretize(data, method=orange.EquiNDiscretization(numberOfIntervals=3))
data = data.select(range(15))
rules = orange.AssociationRulesInducer(data, support=0.4)
orngAssoc.sort(rules, ["support", "confidence"])
orngAssoc.printRules(rules[:40], ["support", "confidence"])
