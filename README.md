# CopyAsKeyboard

## 功能

可以模拟键盘键入复制粘贴文本内容，解决某些网站文本框禁用复制粘贴的问题。

## 使用方法

运行该程序，将需要复制的内容先复制进剪贴板，然后在想要粘贴的文本框里输入 `@@@` ，即可等待程序逐字将剪贴板中内容输入进文本框。

注意，由于`@`需要按住shift按钮输入，而shift按钮在按下的时候会切换英文字母大小写，因此输入字母大小写与当前CapsLock开启状态相反。

## 运行环境

除python外，还需安装pywin32和pynput库。
