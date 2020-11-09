from pomegranate import *

Burglary = DiscreteDistribution( {'T':0.001, 'F':0.999} )
Earthquake = DiscreteDistribution( {'T':0.002, 'F':0.998} )
Alarm = ConditionalProbabilityTable(
    [
        ['T','T','T',0.95],
        ['T','F','T',0.94],
        ['F','T','T',0.29],
        ['F','F','T',0.001],
        ['T','T','F',0.05],
        ['T','F','F',0.06],
        ['F','T','F',0.71],
        ['F','F','F',0.999],
    ], 
    [Burglary, Earthquake]
)

JohnCalls = ConditionalProbabilityTable(
    [
        ['T','T',0.90],
        ['F','T',0.05],
        ['T','F',0.10],
        ['F','F',0.95],
    ], 
    [Alarm]
)
    
MaryCalls = ConditionalProbabilityTable(
    [
        ['T','T',0.70],
        ['F','T',0.01],
        ['T','F',0.30],
        ['F','F',0.99],
    ], 
    [Alarm]
)

s1 = State(Burglary, name="Burglary")
s2 = State(Earthquake, name="Earthquake")
s3 = State(Alarm, name="Alarm")
s4 = State(JohnCalls, name="JohnCalls")
s5 = State(MaryCalls, name="MaryCalls")

model = BayesianNetwork("Burglary")
model.add_states(s1,s2,s3,s4,s5)
model.add_transition(s1,s3)
model.add_transition(s2,s3)
model.add_transition(s3,s4)
model.add_transition(s3,s5)
model.bake()
marginals = model.predict_proba({})

print("P(Alarm) = {}".format(marginals[2].parameters[0]["T"]))

p2 = model.predict_proba({'MaryCalls':'F'})[3].parameters[0]["T"] * marginals[4].parameters[0]["F"]
print("P(J && ~M) = {}".format(p2))

print("P(A | J && ~M) = {}".format(model.predict_proba({'JohnCalls':'T','MaryCalls':'F'})[2].parameters[0]["T"]))

print("P(B | A) = {}".format(model.predict_proba({'Alarm':'T'})[0].parameters[0]["T"]))

p5 = model.predict_proba({'JohnCalls':'T','MaryCalls':'F'})[0].parameters[0]["T"]
print("P(B | J && ~M) = {}".format(p5))

print("P(J && ~M | ~B) = {}".format((1-p5) * p2 / marginals[0].parameters[0]["F"]))