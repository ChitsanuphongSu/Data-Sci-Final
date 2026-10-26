"""Independent arithmetic checks for worked examples and numerical answer keys."""
from math import isclose, exp, log, log2, sqrt
from fractions import Fraction
from questions import QUIZ, MOCK, WRITTEN

checks=0
def selected(items,stem):
    matches=[q for q in items if stem in q['stem']]
    assert len(matches)==1,stem
    q=matches[0]
    return q['options'][q['answer']]
def numeric(items,stem,value):
    global checks
    answer=selected(items,stem)
    assert isclose(float(Fraction(answer)),value,rel_tol=1e-10), (stem,answer,value)
    checks+=1

numeric(QUIZ,'ค่า MAE',sum(abs(x) for x in [1,-2])/2)
numeric(QUIZ,'ค่า MSE',sum(x*x for x in [1,-2])/2)
numeric(QUIZ,'Gaussian σ',.8*2)
numeric(QUIZ,'TP=24, FP=6',24/(24+6))
numeric(QUIZ,'TP=24, FN=16',24/(24+16))
numeric(QUIZ,'โหนดบริสุทธิ์',1-1**2)
numeric(QUIZ,'Logistic z=0',1/(1+exp(0)))
numeric(QUIZ,'F_old=10',10+.1*4)
numeric(QUIZ,'กลุ่มมีค่า [2,4,6]',sum([2,4,6])/3)
numeric(QUIZ,'a=1, b=4',(4-1)/max(1,4))
numeric(QUIZ,'Grid 3×4',3*4*5)
numeric(MOCK,'y=[1,3,5]',1-((1-2)**2+(3-3)**2+(5-4)**2)/((1-3)**2+(3-3)**2+(5-3)**2))
numeric(MOCK,'TP=18, FP=6',2*18/(2*18+6+12))
numeric(MOCK,'ข้อมูล [0,2,10,12]',sum((x-center)**2 for x,center in zip([0,2,10,12],[1,1,11,11])))
assert selected(QUIZ,'PolynomialFeatures degree=3')==str([2,2**2,2**3]).replace(' ','')
assert selected(QUIZ,'neg_mean_squared_error')=='√16=4' and sqrt(16)==4
assert selected(MOCK,'entropy')=='1 bit' and -sum(p*log2(p) for p in [.5,.5])==1
assert 'odds คูณ 2' in selected(MOCK,'β=ln(2)') and isclose(exp(log(2)),2)
checks+=4

# Worked chapter examples, recomputed independently.
assert isclose(1-5/8,.375)
assert isclose(sqrt(5/3),1.2909944487358056)
assert isclose(.5-.6*(1-(1/6)**2-(5/6)**2),1/3)
assert isclose(2*30/(2*30+10+20),2/3)
assert isclose(1-((1-1/100000)**100000),.63212,rel_tol=1e-4)
checks+=5

# W2 answers and rubrics: correct numerical result and exact point totals.
assert isclose((40+130)/(40+20+10+130),.85)
assert isclose(2*40/(2*40+20+10),8/11)
assert '8/11' in WRITTEN[1]['answer']
import re
for w in WRITTEN:
    assert sum(int(re.search(r'\((\d+)\)$',r).group(1)) for r in w['rubric'])==w['points']
checks+=8
print(f'PASS: {checks} independent numeric/formula/rubric checks.')
