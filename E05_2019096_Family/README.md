<h1 align=center>E05 Family Problem ( Prolog )</h1>

|   学号   | 姓名 |    日期    |
| :------: | :--: | :--------: |
| 18340052 | 何泽 | 2020.10.06 |

<h2 align=center>目录</h2>

[TOC]

## Ⅰ About Cousin and Removed

- What Is a First Cousin, Twice Removed?

> If someone walked up to you and said, “Howdy, I’m your third cousin, twice removed,” would you have any idea what they meant? Most people have a good understanding of basic relationship words such as “mother,” “father,” “aunt,” “uncle,” “brother,” and “sister.” But what about the relationship terms that we don’t use in everyday speech? Terms like “second cousin” and “first cousin, once removed”? We don’t tend to speak about our relationships in such exact terms (“cousin” seems good enough when you are introducing one person to another), so most of us aren’t familiar with what these words mean.

- Relationship Terms

> Sometimes, especially when working on your family history, it’s handy to know how to describe your family relationships more exactly. The definitions below should help you out.

- Cousin (a.k.a “first cousin”)

> Your first cousins are the people in your family who have two of the same grandparents as you. In other words, they are the children of your aunts and uncles.

- Second Cousin

> Your second cousins are the people in your family who have the same great-grandparents as you., but not the same grandparents.

- Third, Fourth, and Fifth Cousins

> Your third cousins have the same great great grandparents, fourth cousins have the same great- great-great-grandparents, and so on.

- Removed

> When the word “removed” is used to describe a relationship, it indicates that the two people are from different generations. You and your first cousins are in the same generation (two generations younger than your grandparents), so the word “removed” is not used to describe your relationship.
>
> The words “**once removed**” mean that there is a difference of one generation. For example, your mother’s first cousin is your first cousin, once removed. This is because your mother’s first cousin is one generation younger than your grandparents and you are two generations younger than your grandparents. This one-generation difference equals “once removed.”
>
> **Twice removed** means that there is a two-generation difference. You are two generations younger than a first cousin of your grandmother, so you and your grandmother’s first cousin are first cousins, twice removed.

## Ⅱ Problem Description

Please fulfill the following tasks by using Prolog:

1. Using the predicates male, female, child, and spouse, write facts and rules describing the family tree in Figure 2, and add the fact that William has a daughter Charlotte. Please do not write redundant facts that can be defined with rules.
2. Write rules describing the predicates Grandchild, Greatgrandparent, Ancestor, Sibling, Brother, Sister, Daughter, Son, FirstCousin, BrotherInLaw, SisterInLaw, Aunt, and Uncle.
3. Find out the proper definition of mth cousin n times removed, and write rules to de- fine the predicate mthCousinNremoved(X,Y,M,N). Hint: You’d better define a helper predicate distance(X,Y,N) meaning that there are N generations between X and Y by recursion ( please refer to hanoi.pl).
4. ASK who are Elizabeth’s grandchildren, Diana’s brothers-in-law, Zara’s great-grandparents, Eugenie’s ancestors, and Charlotte’s first cousin once removed.

<img src="/Users/heze/Library/Application Support/typora-user-images/image-20201006135708989.png" alt="image-20201006135708989" style="zoom:50%;" />

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E05_2019096_Family/Family.png" alt="Family" style="zoom:50%;" />

## Ⅲ  Tasks

1. Please complete the Prolog codes. There are several tutorials in the folder and I will explain the usage of Prolog in class.

2. Write the related codes and take a screenshot of the running results in the filenamed E05_YourNumber.pdf, and send it to ai_2020@foxmail.com.

## Ⅳ  Codes

```spreadsheet
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
```

## Ⅴ Results

<img src="/Users/heze/Library/Mobile Documents/com~apple~CloudDocs/大三上/人工智能实验/E05_2019096_Family/截屏2020-10-06 11.34.55.png" alt="截屏2020-10-06 11.34.55" style="zoom:80%;" />

