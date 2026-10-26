# Original practice questions, separate from the instructor assessment.
QUIZ = []
MOCK = []
def q(ch, stem, options, answer, why):
    QUIZ.append(dict(ch=ch, stem=stem, options=options.split('|'), answer=answer, why=why))
def m(ch, stem, options, answer, why):
    MOCK.append(dict(ch=ch, stem=stem, options=options.split('|'), answer=answer, why=why))

q(7,'ระบบกรองสแปม: ข้อใดคือ Experience (E)?','จำนวนสแปมที่จับได้|อีเมลในอดีตพร้อมป้ายกำกับ|งานจำแนกสแปม|ค่า threshold',1,'E คือข้อมูลหรือประสบการณ์ที่ใช้เรียนรู้ ส่วนงานคือ T และตัวชี้วัดคือ P')
q(7,'ต้องการแบ่งลูกค้าเป็นกลุ่มโดยไม่มี label ควรเริ่มจากอะไร?','Regression|Classification|Clustering|Reinforcement learning',2,'ไม่มี target labels และต้องการกลุ่มคล้ายกัน จึงเป็น unsupervised clustering')
q(7,'ทำนาย GPAX ของนักศึกษาเป็นงานใด?','Regression|Binary classification|Clustering|Multilabel classification',0,'GPAX เป็นค่าตัวเลขต่อเนื่อง ต่างจากทำนายเกรดเป็นหมวด A/B/C')
q(7,'Train error ต่ำมาก แต่ validation error สูง สอดคล้องกับอะไร?','Underfitting|ไม่มี noise|Bias สูงเสมอ|Overfitting',3,'โมเดลจำ train ได้ดีแต่ generalize ไม่ดี สอดคล้อง high variance; ต้องตรวจ split/leakage เพิ่ม')
q(7,'StandardScaler ควรใช้กับ validation อย่างไร?','fit ใหม่ด้วย validation|transform ด้วยค่าที่ fit จาก train|fit ด้วย train รวม validation|ไม่ต้อง transform',1,'ใช้ mean/std จาก train เดิม เพื่อให้ preprocessing ตรงกันและไม่รั่ว')
q(7,'LinearRegression.score(X,y) คืนค่าใด?','MAE|Accuracy|R²|RMSE',2,'score ขึ้นกับ estimator สำหรับ LinearRegression คือ R²')
q(7,'Seed คงที่รับประกันอะไรภายใต้ environment และลำดับการสุ่มเดิม?','ทำซ้ำการสุ่มได้|ไม่มี noise|โมเดลดีที่สุด|correlation เท่ากับหนึ่ง',0,'Seed ทำซ้ำได้ ไม่ได้ลด noise หรือรับประกันคุณภาพการทดลอง')
q(7,'การใช้ LLM ช่วยทำ Data Science ที่เหมาะสมคืออะไร?','คัดลอกทุกคำตอบทันที|เชื่อผลรันที่ LLM บอกโดยไม่รัน|ส่งข้อมูลส่วนบุคคลทั้งหมดเพื่อความแม่น|ตรวจโค้ด สูตร ผลจริง และเปิดเผยการใช้ตามกติกา',3,'LLM เป็นผู้ช่วย ผู้วิเคราะห์ยังรับผิดชอบการตรวจสอบและความเป็นส่วนตัว')

q(8,'สมการ ŷ=50+3x เมื่อ x เพิ่มหนึ่งหน่วย ค่าคาดหมายเปลี่ยนเท่าใด?','ลด 3|เพิ่ม 3|เพิ่ม 50|เพิ่ม 53',1,'Slope 3 หมายถึง y เพิ่ม 3 หน่วยต่อ x หนึ่งหน่วยในโมเดล')
q(8,'y=[2,4], ŷ=[1,6] ค่า MAE เท่าใด?','1|2|1.5|2.5',2,'residual=[1,−2]; MAE=(1+2)/2=1.5')
q(8,'จาก residual=[1,−2] ค่า MSE เท่าใด?','2.5|1.5|5|√5',0,'MSE=(1²+(-2)²)/2=2.5; RMSE=√2.5')
q(8,'R²=−0.4 หมายถึงอะไร?','คำนวณผิดเสมอ|ถูก 40%|ทำนายติดลบทุกจุด|แย่กว่า baseline ค่าเฉลี่ยในชุดประเมินตามนิยาม R²',3,'SSE มากกว่า SST จึงติดลบได้ ไม่ใช่เปอร์เซ็นต์ accuracy')
q(8,'Residual เป็นรูปกรวยชี้ไปที่ข้อใด?','ความสัมพันธ์เชิงเส้นสมบูรณ์|ความแปรปรวน error ไม่คงที่|ไม่มี outlier|R² เท่ากับศูนย์',1,'เป็นหลักฐาน heteroscedasticity ไม่ใช่พิสูจน์สาเหตุเพียงอย่างเดียว')
q(8,'PolynomialFeatures degree=3, include_bias=False เมื่อ x=2 ได้อะไร?','[1,2,3]|[2,6,18]|[2,4,8]|[1,2,4,8]',2,'basis คือ x,x²,x³ โดยไม่มีคอลัมน์ค่าคงที่ 1')
q(8,'วิธีใดอาจทำ coefficient เป็นศูนย์พอดี?','Lasso|Ridge เสมอ|OLS เสมอ|StandardScaler',0,'L1 penalty ใน Lasso ทำให้บาง coefficients เป็นศูนย์ได้ ส่วน Ridge มักหดแต่ไม่เป็นศูนย์พอดี')
q(8,'centers ห่าง 2 และ width_factor=.8 แล้ว Gaussian σ เท่าใด?','0.8|2|2.8|1.6',3,'σ=.8×2=1.6; width_factor ไม่ใช่ σ โดยตรง')

q(9,'TP=24, FP=6 ค่า precision คือเท่าใด?','0.6|0.8|0.24|0.75',1,'24/(24+6)=0.8; precision สนใจในกลุ่มที่ทำนาย positive')
q(9,'TP=24, FN=16 ค่า recall คือเท่าใด?','0.8|0.4|0.6|0.24',2,'24/(24+16)=0.6; recall สนใจ positive จริงทั้งหมด')
q(9,'KNN มีรายได้หลักแสนกับอายุหลักสิบ ควรพิจารณาอะไร?','Scaling ภายใน train/fold|เพิ่มรายได้เป็นกำลังสองเสมอ|ใช้ test fit scaler|ลบอายุทันที',0,'ตัวแปรสเกลใหญ่ครอบงำ Euclidean distance; scaling ต้องใช้ train เท่านั้น')
q(9,'เมื่อ k ใน KNN เล็กมาก มักเกิดอะไร?','bias สูงเสมอ|ทุกจุดเป็น negative|ทำนายไม่ใช้ข้อมูล|ไวต่อ noise และ variance สูง',3,'เพื่อนน้อยทำให้ขอบเขตยืดหยุ่นและไวต่อชุดฝึก')
q(9,'โหนดบริสุทธิ์มี Gini เท่าใด?','1|0|0.5|−1',1,'ทุกจุดเป็นคลาสเดียว p=1 จึง Gini=1−1²=0')
q(9,'Logistic z=0 ให้ probability เท่าใด?','0|1|0.5|นิยามไม่ได้',2,'sigmoid(0)=1/(1+1)=.5')
q(9,'ต้องการให้แต่ละคลาสสำคัญเท่ากัน ควรดู average ใด?','Macro|Weighted|Micro เท่านั้น|Accuracy เท่านั้น',0,'Macro เฉลี่ย metric รายคลาสเท่ากัน ส่วน weighted ถ่วงด้วย support')
q(9,'ROC-AUC ควรรับค่าทำนายชนิดใด?','รหัสแถว|residual|ชื่อ feature|probability หรือ decision score',3,'AUC วัด ranking across thresholds การใช้ hard labels ทำให้สูญเสียข้อมูล score')

q(10,'Bagging สร้างชุดฝึกอย่างไร?','สุ่ม y แยกจาก X|สุ่มแถวพร้อมใส่คืน|ใช้ test ฝึกแต่ละต้น|ใช้แถวแรกเสมอ',1,'Bootstrap สุ่มคู่ข้อมูลแถวเดิมพร้อมใส่คืน เพื่อสร้างชุดฝึกหลากหลาย')
q(10,'RF สุ่ม features ที่ขั้นใดเป็นหลัก?','หลังทำนายแล้ว|เฉพาะก่อนแบ่ง test|ตอนพิจารณา split แต่ละ node|เฉพาะเลือก metric',2,'การสุ่ม features ต่อ split ช่วยลด correlation ระหว่างต้น')
q(10,'ทำไมโมเดลที่ผิดเหมือนกันทั้งหมดจึงรวมแล้วไม่ช่วยมาก?','ไม่มี diversity ของ errors|เพราะจำนวนต้องเป็นเลขคู่|เพราะห้ามใช้โมเดลซ้ำชนิด|เพราะทุก ensemble ลด bias เท่านั้น',0,'การเฉลี่ยไม่ลบข้อผิดพลาดที่สัมพันธ์กันทั้งหมด')
q(10,'F_old=10, correction=4, learning_rate=.1 ได้ F_new เท่าใด?','14|4|1.4|10.4',3,'F_new=10+.1×4=10.4')
q(10,'Early stopping ควรดูชุดใด?','final test|validation|future production labels ทั้งหมด|training accuracy เท่านั้น',1,'validation เป็นส่วนเลือกจำนวนรอบ final test ต้องไม่ช่วยเลือก')
q(10,'Feature importance สูงยืนยันอะไรได้มากที่สุด?','เป็นเหตุของ y|เพิ่ม feature แล้ว y จะเพิ่มแน่|โมเดลพึ่ง feature นั้นตามนิยาม importance ที่ใช้|feature ไม่มี leakage',2,'ความสำคัญเป็นพฤติกรรมของโมเดล ไม่พิสูจน์เหตุและผลหรือทิศทาง')
q(10,'Stacking ควรฝึก meta-model ด้วยอะไร?','Out-of-fold predictions|Test labels|Train predictions ที่แต่ละ base model จำมาเสมอ|ชื่อโมเดลอย่างเดียว',0,'OOF predictions มาจากโมเดลที่ไม่เคยฝึกบนแถวนั้น ช่วยลด optimistic leakage')
q(10,'OOB fraction ของ bootstrap n ครั้งเมื่อ n ใหญ่ใกล้เท่าใด?','100%|0%|63.2%|36.8%',3,'ความน่าจะเป็นที่แถวไม่ถูกเลือก=(1−1/n)^n≈e^-1≈.368')

q(11,'K-Means ลดค่าใด?','Classification accuracy|ผลรวมระยะกำลังสองถึง centroid|จำนวน labels จริง|MAE ของ target',1,'Objective คือ within-cluster sum of squared Euclidean distances หรือ inertia')
q(11,'กลุ่มมีค่า [2,4,6] centroid คืออะไร?','2|6|4|12',2,'Centroid คือค่าเฉลี่ย (2+4+6)/3=4')
q(11,'เมื่อเพิ่ม K โดยทั่วไป inertia เป็นอย่างไรเมื่อหาคำตอบเหมาะสม?','ไม่เพิ่มและมักลด|เพิ่มเสมอ|ต้องเป็นหนึ่ง|กลายเป็น accuracy',0,'จำนวนกลุ่มมากขึ้นมีอิสระมากขึ้นจึงลด objective ได้ แต่คุณค่าการจัดกลุ่มไม่ได้ดีขึ้นเสมอ')
q(11,'a=1, b=4 silhouette เท่าใด?','4|0.25|−0.75|0.75',3,'(4−1)/max(1,4)=.75')
q(11,'Cluster 2 สูงกว่า Cluster 1 หรือไม่?','สูงกว่าเสมอ|เลขเป็นเพียง label ไม่มีอันดับ|ต่ำกว่าเสมอ|ขึ้นกับจำนวน feature เท่านั้น',1,'หมายเลข cluster สลับได้ ต้องดู profile ก่อนตั้งชื่อหรือความหมาย')
q(11,'ก่อนตีความ standardized centroids ในหน่วยเงินบาทควรทำอะไร?','คูณ K|หาร silhouette|inverse_transform ด้วย scaler เดิม|เปลี่ยน label',2,'คืนสเกลด้วย mean/std เดิมจึงกลับเป็นหน่วยต้นฉบับ')
q(11,'η² บอกอะไร?','ขนาดความสัมพันธ์ของกลุ่มกับความแปรปรวนในข้อมูล|ความน่าจะเป็นที่ H₀ จริง|สาเหตุแน่นอนของผล|accuracy',0,'η²=SS_between/SS_total เป็น effect size ไม่ใช่ p-value หรือ causality')
q(11,'ข้อใดเป็นการยืนยันกลุ่มที่อ่อนที่สุด?','ดู stability|หารือ domain expert|ดูผลลัพธ์ภายนอก|สร้างกลุ่มจากรายได้ แล้วใช้ p-value รายได้บนข้อมูลเดิมยืนยันอิสระ',3,'การแยกตามรายได้สร้างความต่างอยู่แล้ว เป็น circular analysis ควรตีความเชิงสำรวจ')

q(12,'ข้อมูลผู้ป่วยหนึ่งคนหลายครั้ง ต้อง generalize ไปคนใหม่ ควร split แบบใด?','สุ่มรายแถวเสมอ|แบ่งตาม patient group|แยกเลขแถวคู่คี่|ให้คนเดิมอยู่ทุก fold',1,'ต้องกันคนเดียวกันไม่ให้ข้าม train/validation เพื่อจำลองผู้ป่วยใหม่')
q(12,'ทำนายอนาคตจากอดีต ควรเริ่มพิจารณาอะไร?','Random shuffle เท่านั้น|LOOCV เท่านั้น|Temporal split / TimeSeriesSplit|เอาอนาคต train อดีต test',2,'ลำดับเวลาต้องสะท้อนข้อมูลที่รู้ได้ขณะทำนาย')
q(12,'Grid 3×4 candidates ใช้ 5 folds มีกี่ CV fits ไม่รวม refit?','60|12|5|17',0,'12 combinations×5 folds=60')
q(12,'CV scoring neg_mean_squared_error ได้ −16 แปลงเป็น RMSE อย่างไร?','−4|16|−16|√16=4',3,'กลับเครื่องหมายก่อนถอดราก ห้ามถอดรากของค่าติดลบ')
q(12,'best_score_ ของ GridSearchCV คืออะไร?','Final test score|CV mean ของ candidate ที่ชนะ|training loss ทุกจุด|accuracy เสมอ',1,'เป็นคะแนนจากการเลือกแบบบน development ไม่ใช่ final test estimate')
q(12,'ข้อใด Pipeline ไม่แก้ให้เอง?','fit scaler ใน fold|เรียง transformer|feature ที่บอกผลอนาคตอยู่แล้ว|ใช้ transform ตอน predict',2,'Pipeline ป้องกัน learned preprocessing leakage ไม่ได้รู้ว่า feature มี target/future information')
q(12,'Learning curve ใช้อะไรเป็นแกน x?','จำนวนตัวอย่างฝึก|max_depth เสมอ|จำนวนคลาสเสมอ|test accuracy',0,'Learning curve เปลี่ยนขนาด training set; validation curve เปลี่ยน hyperparameter')
q(12,'Mean±std จาก 5 CV folds คือ 95% CI เสมอหรือไม่?','ใช่เพราะมีห้า folds|ใช่เพราะใช้ seed|ใช่ถ้า score สูง|ไม่ใช่ เป็นความกระจายระหว่าง folds',3,'fold scores ไม่ได้อิสระทั้งหมดและ mean±std ไม่ใช่สูตร 95% CI โดยอัตโนมัติ')

# 24 new multiple-choice questions, 2.5 points each = 60 points.
m(7,'ต้องเรียนรู้นโยบายเลือก action จาก reward สะสม จัดเป็นอะไร?','Supervised regression|Clustering|Reinforcement learning|PCA',2,'RL เชื่อม agent/state/action/reward เพื่อเป้าหมายผลตอบแทนสะสม')
m(7,'ข้อมูลหนึ่ง feature 80 ตัวอย่าง X ควรมี shape ใด?','(80,1)|(1,80)|(80,80)|scalar',0,'แถวคือตัวอย่าง คอลัมน์คือ features')
m(7,'โมเดล train/validation error สูงใกล้กัน ควรลองอะไรก่อนตามหลัก bias–variance?','เพิ่ม penalty ให้แรงมาก|เพิ่ม features ที่เกี่ยวข้องหรือเพิ่มความยืดหยุ่น|เพิ่ม test เข้า train ก่อนเลือก|ลดข้อมูลให้เหลือครึ่ง',1,'อาการสอดคล้อง high bias จึงปรับ representation หรือ model capacity')
m(7,'ต้องพยากรณ์วันพรุ่งนี้เวลา 20:00 วันนี้ feature ใดใช้ได้?','อุณหภูมิจริงเฉลี่ยพรุ่งนี้|ยอดจริงพรุ่งนี้|residual พรุ่งนี้|พยากรณ์อากาศที่เผยแพร่ก่อน 20:00 วันนี้',3,'ต้องรู้ feature ณ เวลาทำนาย ตัวเลือกอื่นเกิดภายหลัง')
m(8,'y=[1,3,5], ŷ=[2,3,4] ค่า R² เป็นเท่าใด?','0.25|0.5|0.75|1',2,'SSE=2, ȳ=3, SST=8 → R²=1−2/8=.75')
m(8,'สมการ ŷ=8−2x+5z สัมประสิทธิ์ x ตีความอย่างไร?','เพิ่ม x 1 หน่วย ค่าคาดหมาย y ลด 2 เมื่อ z คงที่|เพิ่ม x แล้ว y ลดเสมอเชิงเหตุผล|x มีค่า −2|y ติดลบเสมอ',0,'เป็น conditional association ของแบบจำลอง ไม่ยืนยัน causality')
m(8,'เปรียบเทียบ penalty บน Gaussian basis ให้แยกสาเหตุได้ ควรทำอย่างไร?','เปลี่ยน N ทุกโมเดล|ตรึง basis/scaler/split และเปลี่ยนเฉพาะ penalty ตามโจทย์|fit centers บน test|ใช้ alpha เท่ากันแล้วสรุปเท่าแรงกัน',1,'ต้องควบคุมตัวแปรอื่นเพื่อแยกผลของ penalty')
m(8,'Ordinary pairs bootstrap ควรสุ่มอย่างไร?','สุ่ม X และ y คนละ indices|สุ่ม residual final test|ใช้ coefficient เดิมซ้ำ|สุ่มแถว X,y คู่กันแบบใส่คืน',3,'รักษาความสัมพันธ์ X กับ y ภายใน observation แต่ ordinary bootstrap สมมติ independence ระหว่างแถว')
m(9,'TP=18, FP=6, FN=12 ค่า F1 คือเท่าใด?','0.5|0.75|2/3|0.9',2,'F1=36/(36+6+12)=36/54=2/3')
m(9,'สองคลาสสัดส่วน .5/.5 ให้ entropy เท่าใดเมื่อใช้ log₂?','1 bit|0|0.5 bit|2 bits',0,'−.5log₂(.5)−.5log₂(.5)=1')
m(9,'Single-label multiclass รวมทุก class ค่า micro F1 เทียบ accuracy อย่างไร?','ต่ำกว่าเสมอ|เท่ากัน|สูงกว่าเสมอ|ไม่เกี่ยวข้อง',1,'เมื่อรวมทุกคลาสแต่ละข้อผิดสร้างหนึ่ง FP และหนึ่ง FN จึง micro P/R/F1 เท่ากับ accuracy')
m(9,'Logistic coefficient β=ln(2) เมื่อ feature เพิ่ม 1 หน่วย odds เปลี่ยนอย่างไร?','probability เพิ่ม 2 เสมอ|odds ลดครึ่ง|probability เพิ่ม 50 จุดเสมอ|odds คูณ 2 เมื่อ features อื่นคงที่',3,'log-odds เปลี่ยน β ดังนั้น odds คูณ exp(β)=2')
m(10,'การแก้ residual แบบ y−F ตรง ๆ ใน gradient boosting ตรงกับ loss ใดมากที่สุด?','Accuracy|Silhouette|Squared error|Gini ทั้ง ensemble',2,'Squared error มี negative gradient เป็นสัดส่วนกับ residual; loss อื่นใช้ gradient ของ loss นั้น')
m(10,'ความสัมพันธ์ errors ระหว่าง trees สูงมาก ส่งผลอย่างไร?','ประโยชน์จากการเฉลี่ยลดลง|รับประกัน test 100%|ไม่ต้องเพิ่ม diversity|ทำให้โมเดลเป็น linear',0,'correlated errors ลดกันไม่ได้มากเมื่อเฉลี่ย')
m(10,'ต้องการจำกัดขนาดใบของ forest ให้ smooth ขึ้น ควรลองอะไร?','ลด min_samples_leaf เป็น 1 เสมอ|เพิ่ม min_samples_leaf|เพิ่ม target เป็น feature|เพิ่ม n_jobs เพื่อ regularize',1,'ใบต้องมีตัวอย่างมากขึ้นจึงลดการ fit noise เฉพาะจุด')
m(10,'Permutation importance ที่สูงหมายถึงอะไรโดยตรง?','feature ทำให้เกิดผลเชิงสาเหตุ|feature มี coefficient บวก|feature ไม่มีข้อมูลรั่ว|การสลับ feature ทำให้ metric แย่ลงมากในชุดที่วัด',3,'บอก dependence ของโมเดลต่อ feature ภายใต้ข้อมูลและ metric นั้น')
m(11,'ข้อมูล [0,2,10,12], กลุ่ม [0,2] และ [10,12] มี inertia เท่าใด?','2|8|4|0',2,'centers=1,11; ระยะกำลังสองแต่ละจุด=1 รวมเป็น4')
m(11,'Silhouette ติดลบสื่ออะไร?','จุดอาจใกล้กลุ่มอื่นมากกว่ากลุ่มตัวเอง|ต้องมี missing|K=1 เสมอ|โมเดลเป็น classifier',0,'a>b ทำให้ b−a ติดลบ')
m(11,'ANOVA reject H₀ สรุปข้อใดได้ภายใต้ assumptions?','ทุกคู่ต่างกัน|อย่างน้อยหนึ่งค่าเฉลี่ยกลุ่มต่าง|ทุก median ต่าง|เป็นเหตุและผล',1,'Omnibus test ไม่บอกคู่ที่ต่าง ต้องทำ post-hoc ที่เหมาะหากต้องการระบุคู่')
m(11,'คะแนน K=7 สูงกว่า K=4 เล็กน้อย แต่ทีมรองรับ 4 segments ควรทำอะไร?','เลือก 7 โดยไม่สนทรัพยากร|เลือก 4 แล้วซ่อนคะแนน|ลบ 3 clusters|เปรียบเทียบคุณภาพ ความเสถียร และ actionability แล้วอธิบาย trade-off',3,'ต้องผสาน evidence และข้อจำกัดจริง ไม่อ้างว่าคะแนนภายในเป็นเกณฑ์เดียว')
m(12,'เลือกโมเดลจาก test 20 แบบแล้วรายงานตัวที่ดีที่สุด ทำให้เกิดอะไร?','ประเมินอิสระขึ้น|ลด selection bias|test กลายเป็นส่วนของการเลือกแบบ|เป็น nested CV',2,'การเลือกจาก test ทำให้ estimate optimistic และไม่ใช่ unseen final test อีกต่อไป')
m(12,'แบบ A CV=.84±.01 แบบ B=.841±.08 และ B แพงกว่ามาก ควรสรุปอย่างไร?','พิจารณา A เพราะใกล้เคียง เสถียรและง่ายกว่า โดยไม่อ้างนัยสำคัญจากตัวเลขนี้อย่างเดียว|B ชนะแน่|A มี accuracy 100%|ต้องเฉลี่ย test เข้า CV',0,'เปรียบเทียบ cost/stability/simplicity ไม่ไล่ทศนิยมโดยมองข้าม uncertainty')
m(12,'Nested CV ใช้ inner และ outer อย่างไร?','outer tune, inner final test|inner เลือก hyperparameters, outer ประเมินกระบวนการ|ทั้งคู่ train บนทุกแถว|ใช้ test เดิมทุก fold',1,'outer holdout ไม่เข้าการเลือกภายในรอบนั้น')
m(12,'Early stopping กับการเลือก threshold จัดเป็นขั้นใด?','final reporting เท่านั้น|ไม่เกี่ยวข้อง validation|ทำได้เฉพาะ unsupervised|model selection ที่ต้องใช้ development/validation',3,'ทั้งสองมีผลต่อแบบที่ใช้จริง จึงห้ามใช้ final test ตัดสิน')

WRITTEN = [
dict(title='W1 · ออกแบบ regression pipeline',points=8,prompt='มีข้อมูลการใช้ไฟฟ้ารายวัน ต้องทำนายวันพรุ่งนี้ด้วยข้อมูลที่มีเวลา 20:00 วันนี้ อธิบาย target, features, split, preprocessing, baseline, metric, วิธีเลือกแบบ และ final test',answer='Target=พลังงานวันพรุ่งนี้ (kWh); ใช้พยากรณ์อากาศที่เผยแพร่ทันเวลาและปฏิทิน ไม่ใช้ค่าจริงวันพรุ่งนี้ แบ่งตามเวลา Fit preprocessing เฉพาะ train/fold เริ่ม baseline ค่าเฉลี่ยหรือ linear เลือกด้วย validation RMSE และรายงาน MAE/R² ประกอบ ล็อกแบบแล้วใช้ final test หนึ่งครั้ง',rubric=['target + เวลาใช้งานชัดเจน (1)','features พร้อมใช้งาน ไม่มีอนาคต (1)','temporal split ถูกต้อง (1)','preprocessing fit train/fold (1)','baseline สมเหตุผล (1)','metric และหน่วยถูกต้อง (1)','selection ใช้ validation (1)','final test หลังล็อกแบบ (1)']),
dict(title='W2 · คำนวณและตีความ classification',points=8,prompt='กำหนด positive คือ fraud มี TP=40, FP=20, FN=10, TN=130 คำนวณ accuracy, precision, recall, F1 แล้วอธิบายว่าจะเน้น metric ใดถ้าพลาด fraud แพง พร้อมวิธีเลือก threshold',answer='N=200; accuracy=170/200=.85; precision=40/60=2/3; recall=40/50=.8; F1=80/(80+20+10)=8/11≈.7273 เน้น recall เพื่อลด FN แต่จำกัด FP/ต้นทุนตรวจสอบ เลือก threshold ด้วย validation ที่สะท้อนสัดส่วนจริง แล้วทดสอบหลังล็อก threshold',rubric=['accuracy ถูกต้อง (1)','precision ถูกต้อง (1)','recall ถูกต้อง (1)','F1 ถูกต้อง (1)','โยงต้นทุน FN กับ recall (1)','กล่าวถึง FP/ต้นทุน trade-off (1)','เลือก threshold จาก validation (1)','test หลังล็อก threshold (1)']),
dict(title='W3 · Debug leakage',points=8,prompt='โค้ดทำ scaler.fit_transform(X) ก่อน split จากนั้นวน degree 1–12 เลือกตัวที่ test RMSE ต่ำสุด อธิบายปัญหาสองจุดและเขียน pseudocode กระบวนการที่ถูกต้อง',answer='จุดแรก scaler เรียนรู้จาก test จุดที่สองใช้ test เลือก degree แก้โดยกัน test ก่อน ส่ง Pipeline(poly→scale→regressor) เข้า CV บน development ใช้ folds ที่ตรงเวลา/กลุ่ม เลือก degree จาก CV แล้ว refit บน development หาก protocol อนุญาต ประเมิน test ของแบบที่ล็อกแล้ว',rubric=['ระบุ preprocessing leakage (2)','ระบุ test-based selection (2)','Pipeline อยู่ภายใน CV พร้อมเลือก split เหมาะ (2)','refit ตาม protocol และ test ครั้งสุดท้าย (2)']),
dict(title='W4 · Clustering ที่อธิบายได้',points=6,prompt='จัดลูกค้าด้วยอายุ รายได้ และยอดซื้อโดย K-Means แล้วจะยืนยันว่ากลุ่มดีได้อย่างไร? อธิบาย scaling, เลือก K, profiling และข้อจำกัดการใช้ ANOVA กับ features ที่ใช้สร้างกลุ่ม',answer='ตรวจหน่วย/outlier และ scale อย่างมีเหตุผล เปรียบเทียบ inertia/elbow, silhouette, stability และความเหมาะกับงาน สรุปขนาดกลุ่มและ centers ในหน่วยเดิม ตั้งชื่อเชิงพฤติกรรม ร่วม domain expert วาง action การทดสอบ features เดิมที่ใช้สร้างกลุ่มมี selection/circularity จึงไม่ใช่การยืนยันอิสระ',rubric=['scaling และความหมาย distance (1)','เลือก K หลายหลักฐาน (2)','profiling/หน่วยเดิม/domain action (2)','ข้อจำกัด circular testing (1)']),
dict(title='W5 · ออกแบบการเทียบ Gaussian penalty',points=6,prompt='ต้องเปรียบเทียบ OLS/Ridge/Lasso ตาม P05 ระบุสิ่งที่ต้องตรึง ขั้นตอนเลือกแบบ และข้อห้าม final test รวมทั้งเหตุใด alpha เท่ากันไม่ได้เทียบแรงตรง ๆ',answer='ตรึงข้อมูล seeds/splits, N=12, width_factor=.8 และ centers/scaler ที่ fit จาก train เดียวกัน เปรียบเทียบ train/validation RMSE ของ OLS, Ridge(.1), Lasso(.001) เลือก validation ต่ำสุดโดย tie≤1e−6 ตาม OLS→Ridge→Lasso ใช้โมเดล/basis/scaler เดิมทดสอบ seed43 ไม่ refit Ridge/Lasso ใช้รูป penalty และ normalization ต่างกัน',rubric=['ตรึง basis/splits/scaler จาก train (2)','validation selection และ tie rule (1)','ไม่ refit / ไม่เลือกจาก test (2)','objective normalization/penalty ต่าง (1)']),
dict(title='W6 · วิเคราะห์ bias–variance และ ensemble',points=4,prompt='ต้นไม้ train accuracy=1.00, validation=.67 อธิบายอาการและเสนอการแก้สองแนวทาง พร้อมเหตุผลว่าทำไม forest อาจช่วยและทำไมยังไม่รับประกัน',answer='สอดคล้อง overfit/high variance; จำกัด depth/เพิ่ม min_samples_leaf และลอง bagging/Random Forest หรือข้อมูลเพิ่มที่เหมาะ RF เฉลี่ยต้นที่มีความหลากหลายจาก bootstrap+feature sampling ช่วยลด variance แต่ยังเสี่ยง leakage, shift และ correlated errors ต้องประเมิน validation เดิม',rubric=['วินิจฉัย high variance (1)','สองแนวทางมีเหตุผล (1)','กลไก diversity/averaging (1)','ไม่รับประกันและต้อง validate (1)'])
]
