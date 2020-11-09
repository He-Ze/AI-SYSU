male('George').
male('Kydd').
male('Philip').
male('Charles').
male('William').
male('Mark').
male('Harry').
male('Peter').
male('Andrew').
male('Edward').
male('James').

female('Mum').
female('Spencer').
female('Elizabeth').
female('Margaret').
female('Diana').
female('Anne').
female('Zara').
female('Sarah').
female('Beatrice').
female('Eugenie').
female('Sophie').
female('Louise').
female('Charlotte').
female('Kate').

child('Elizabeth','George').
child('Elizabeth','Mum').
child('Margaret','George').
child('Margaret','Mum').
child('Diana','Spencer').
child('Diana','Kydd').
child('Charles','Elizabeth').
child('Charles','Philip').
child('Anne','Elizabeth').
child('Anne','Philip').
child('Andrew','Elizabeth').
child('Andrew','Philip').
child('Edward','Elizabeth').
child('Edward','Philip').
child('William','Diana').
child('William','Charles').
child('Harry','Diana').
child('Harry','Charles').
child('Peter','Anne').
child('Peter','Mark').
child('Zara','Anne').
child('Zara','Mark').
child('Beatrice','Andrew').
child('Beatrice','Sarah').
child('Eugenie','Andrew').
child('Eugenie','Sarah').
child('Louise','Edward').
child('Louise','Sophie').
child('James','Edward').
child('James','Sophie').
child('Charlotte','William').
child('Charlotte','Kate').

spouse('George','Mum').
spouse('Spencer','Kydd').
spouse('Elizabeth','Philip').
spouse('Diana','Charles').
spouse('Anne','Mark').
spouse('Andrew','Sarah').
spouse('Edward','Sophie').
spouse('William','Kate').
spouses(A,B):-spouse(A,B);spouse(B,A).

grandchild(A,B):-child(A,C),child(C,B).
greatgrandparent(A,B):-child(B,C),grandchild(C,A).
ancestor(A,B):-child(B,A).
ancestor(A,B):-child(B,C),ancestor(A,C).
sibling(A,B) :- child(A,C), child(B,C), A \== B.
brother(A,B):-male(A),sibling(A,B).
sister(A,B):-female(A),sibling(A,B).
daughter(A,B):-female(A),child(A,B).
son(A,B):-male(A),child(A,B).
firstCousin(A,B):-child(A,C),child(B,D),sibling(C,D).
brotherInLaw(A,B):-brother(A,C),spouses(B,C).
sisterInLaw(A,B):-sister(A,C),spouses(B,C).
aunt(A,B):-child(B,C),sister(A,C).
aunt(A,B):-child(B,C),sisterInLaw(A,C).
uncle(A,B):-child(B,C),brother(A,C).
uncle(A,B):-child(B,C),brotherInLaw(A,C).

distance(A, A, 0).
distance(A, B, 0):-spouse(A,B);sibling(A,B).
distance(A, B, 0):-firstCousin(A,C),spouse(C,B).
distance(A, B, 0):-child(A,C),child(B,D),spouse(C,D).
distance(A, B, 0):-child(A,C),child(B,D),sibling(C,D).
distance(A, B, 0):-child(A,C),child(B,D),firstCousin(C,D).
distance(A, B, K):-child(A, C), distance(C, B, K1), K is K1+1.
distance(A, B, K):-child(B, C), distance(C, A, K1), K is K1+1.

mthCousinNremoved(X, Y, M, N):-distance(C,X,M+1),distance(C,Y,M+N+1),\+mthCousinNremoved(X,Y,M-1,N).
