import pandas as pd
file_path = "D:\桌面那些东西\丰.xlsx"
data = pd.read_excel(file_path)
# 创建一个新的目标变量，指示当前周期的销售额是否超过前一个周期
data['是否超过上一期'] = data['销售额'].diff() > 0

# 显示包含新目标变量的更新后数据框

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# 将 '开奖日期' 转换为 datetime 格式
data['开奖日期'] = pd.to_datetime(data['开奖日期'])

# 从日期中提取特征，例如月份和星期几
data['月份'] = data['开奖日期'].dt.month
data['星期'] = data['开奖日期'].dt.weekday

# 准备特征和目标变量以训练模型
X = data[['月份', '星期', '销售额']]
y = data['是否超过上一期']

# 假设X是特征矩阵，y是目标变量（1表示增高，0表示降低）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建C4.5决策树模型
clf = DecisionTreeClassifier(criterion="entropy")

# 训练模型
clf.fit(X_train, y_train)

# 使用模型预测测试集的概率
probabilities = clf.predict_proba(X_test)

# probabilities是一个二维数组，每一行对应一个样本，每一列对应一个类别的概率
# 我们只关心类别为1（增高）的概率
probabilities_increase = probabilities[:, 1]

# 现在你有了每个测试样本被预测为增高的概率
# 你可以根据这些概率来评估模型的性能，例如通过计算预测概率的阈值来调整准确度与召回率

# 评估模型准确度
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"模型准确度  {accuracy}")

# 打印前几个样本的预测概率
print("样本增加概率：")
for i in range(45):
    print(f"样本 {i}: 增加的概率 = {probabilities_increase[i]:.4f}")

