import numpy as np  

def nth_degree_polynomial(x, b, w):
    """
    计算 1 元 N 次多项式：y = b + w[0]*x + w[1]*x^2 + ... + w[N-1]*x^N
    """ 
    degree = len(w)
    y_hat = np.zeros_like(x, dtype=float)
    
    for i in range(degree):
        y_hat += w[i] * (x ** (i + 1))
    
    y_hat += b
    return y_hat

def loss_function(x, b, w, y, regularization=0.0):  
    """
    计算损失函数（均方差损失 + L2正则化）
    """
    y_hat = nth_degree_polynomial(x, b, w)
    mse = np.mean((y_hat - y) ** 2)
    reg_term = regularization * np.sum(w**2)
    return mse + reg_term

def gradient_descent(x, b, w, y, regularization, steps, alpha):  
    """
    使用数值微分的梯度下降优化（带梯度裁剪）
    """
    print(f"开始梯度下降优化...")
    print(f"初始参数: b={b:.4f}, w={w}")
    print(f"初始损失: {loss_function(x, b, w, y, regularization):.6f}")
    
    delta = 1e-7  # 数值微分的微小增量
    grad_clip = 10.0  # 梯度裁剪阈值
    
    # 记录损失历史
    loss_history = []
    
    for i in range(steps):
        # ===== 计算b的梯度 =====
        loss_b_plus = loss_function(x, b + delta, w, y, regularization)
        loss_b = loss_function(x, b, w, y, regularization)
        dL_db = (loss_b_plus - loss_b) / delta
        
        # ===== 计算w的梯度 =====
        dL_dw = np.zeros_like(w)
        for j in range(len(w)):
            w_plus = w.copy()
            w_plus[j] = w[j] + delta
            
            loss_w_plus = loss_function(x, b, w_plus, y, regularization)
            loss_w = loss_function(x, b, w, y, regularization)
            dL_dw[j] = (loss_w_plus - loss_w) / delta
        
        # ===== 梯度裁剪 =====
        dL_db = np.clip(dL_db, -grad_clip, grad_clip)
        dL_dw = np.clip(dL_dw, -grad_clip, grad_clip)
        
        # ===== 更新参数 =====
        w -= alpha * dL_dw
        b -= alpha * dL_db
        
        # 每100步显示进度
        if (i + 1) % 100 == 0:
            current_loss = loss_function(x, b, w, y, regularization)
            loss_history.append(current_loss)
            print(f"第 {i+1:4d} 步: 损失 = {current_loss:.6f}")
    
    return b, w, loss_history

def format_polynomial(b, w):
    """格式化多项式为可读字符串"""
    terms = []
    
    # 处理常数项b
    if abs(b) > 1e-10:
        terms.append(f"{b:+.4f}")
    
    # 处理各次项
    for i, weight in enumerate(w):
        power = i + 1
        if abs(weight) > 1e-10:  # 只显示非零项
            if power == 1:
                terms.append(f"{weight:+.4f}*x")
            else:
                terms.append(f"{weight:+.4f}*x^{power}")
    
    if not terms:
        return "y = 0"
    
    expression = "y = " + terms[0]
    for term in terms[1:]:
        if term[0] != '-':
            expression += " + " + term
        else:
            expression += " " + term
    
    return expression

# ===== 数据标准化 =====
def standardize_data(x, y):
    """标准化数据"""
    x_mean = np.mean(x)
    x_std = np.std(x)
    x_scaled = (x - x_mean) / x_std
    
    y_mean = np.mean(y)
    y_std = np.std(y)
    y_scaled = (y - y_mean) / y_std
    
    return x_scaled, y_scaled, (x_mean, x_std, y_mean, y_std)

def unstandardize_coefficients(b, w, scaling_params):
    """将标准化后的系数还原为原始尺度"""
    x_mean, x_std, y_mean, y_std = scaling_params
    
    # 将标准化后的多项式转换回原始尺度
    # y_orig = y_scaled * y_std + y_mean
    # y_scaled = b + w[0]*x_scaled + w[1]*x_scaled^2 + ...
    # x_scaled = (x_orig - x_mean) / x_std
    
    # 重新计算原始尺度的系数
    w_orig = w.copy()
    b_orig = b
    
    # 需要展开多项式并进行系数转换
    # 这是一个复杂的过程，对于高次多项式，我们直接使用数值方法
    return b_orig, w_orig

# 原始测试数据
x_orig = np.arange(1, 13, dtype=float)
y_orig = np.array([1.9, 8.7, 6.7, 21.7, 21.6, 29.6, 30.0, 28.0, 21.1, 23.7, 13.1, 10.6], dtype=float)

# 数据标准化
x_scaled, y_scaled, scaling_params = standardize_data(x_orig, y_orig)
print(f"数据标准化完成:")
print(f"x均值={scaling_params[0]:.2f}, x标准差={scaling_params[1]:.2f}")
print(f"y均值={scaling_params[2]:.2f}, y标准差={scaling_params[3]:.2f}")

# 初始化参数（使用更小的值）
b = 0.0
degree = 2
w = np.random.normal(0, 0.1, degree)  # 使用小的随机初始值

# 运行梯度下降
regularization = 0.01  # 正则化系数
steps = 1000  # 迭代次数
alpha = 0.01  # 更小的学习率

b_opt, w_opt, loss_history = gradient_descent(x_scaled, b, w, y_scaled, regularization, steps, alpha)

print(f"\n" + "="*50)
print(f"优化完成!（在标准化数据上）")
print(f"最终参数: b = {b_opt:.6f}")
print(f"最终权重: w = [{', '.join(f'{w:.6f}' for w in w_opt)}]")
print(f"最终损失: {loss_function(x_scaled, b_opt, w_opt, y_scaled, regularization):.8f}")

print(f"\n标准化尺度下的预测函数：")
print(format_polynomial(b_opt, w_opt))

# 预测标准化数据
y_pred_scaled = nth_degree_polynomial(x_scaled, b_opt, w_opt)

# 反标准化
def predict_original(x, b, w, scaling_params):
    """预测原始尺度的y值"""
    x_mean, x_std, y_mean, y_std = scaling_params
    x_scaled = (x - x_mean) / x_std
    y_scaled = nth_degree_polynomial(x_scaled, b, w)
    return y_scaled * y_std + y_mean

# 计算原始尺度的预测
y_pred_orig = predict_original(x_orig, b_opt, w_opt, scaling_params)

# 计算R²分数
def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

r2 = r2_score(y_orig, y_pred_orig)
print(f"\n原始尺度R²分数: {r2:.6f}")

# 可视化验证
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'SimHei'

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 子图1：拟合曲线
ax1 = axes[0]
x_plot = np.linspace(0.5, 12.5, 200)
y_plot = predict_original(x_plot, b_opt, w_opt, scaling_params)

ax1.scatter(x_orig, y_orig, color='red', label='原始数据', s=60, zorder=5)
ax1.plot(x_plot, y_plot, 'b-', label='拟合曲线', linewidth=2)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title(f'多项式拟合 (R²={r2:.4f})')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0.5, 12.5)

# 子图2：损失下降曲线
ax2 = axes[1]
ax2.plot(range(100, steps+1, 100), loss_history, 'r-', linewidth=2)
ax2.set_xlabel('迭代步数')
ax2.set_ylabel('损失函数值')
ax2.set_title('损失函数下降曲线')
ax2.grid(True, alpha=0.3)
ax2.set_yscale('log')

# 子图3：残差图
ax3 = axes[2]
residuals = y_pred_orig - y_orig
ax3.scatter(x_orig, residuals, color='green', s=50)
ax3.axhline(y=0, color='r', linestyle='--', alpha=0.5)
ax3.set_xlabel('x')
ax3.set_ylabel('残差 (预测-真实)')
ax3.set_title('残差图')
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
