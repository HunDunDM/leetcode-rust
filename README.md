# My Leetcode Solution in Rust

# 参考

项目结构以及template参考了[aylei](https://github.com/aylei)的[leetcode-rust](https://github.com/aylei/leetcode-rust)项目，感谢大佬

# 环境

* System: macOS
* IDE：CLion(with Rust Plugin)
* Python: 3.7

# 使用

* ~~PyCharm会自动建立该项目的Python venv环境~~
* `python3.7 -m venv venv`已更换为jetbrains官方更推荐的CLion，需要手动建立
* `pip install -r requirements.txt` 安装所需的py组件
* `python new.py {id}` 生成对应题目的模板（需要进入pyvenv环境）
* `cargo test test_{id}` 运行测试样例

# 目录

* [1 - Two Sum](./src/p0001_two_sum.rs)
* [2 - Add Two Numbers](./src/p0002_add_two_numbers.rs)
