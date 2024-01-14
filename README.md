This is a simple script that parses a Jekyll post written in markdown and sends it to a telegram channel.

Is was quite frustrating to copy these posts manually. Reasons:
1. Telegram Desktop [does not support](https://github.com/telegramdesktop/tdesktop/issues/4737) markdown links formatting: `[text](http://example.com)`. You should manually paste links [using hotkeys](https://github.com/telegramdesktop/tdesktop/issues/4336). That is really annoyng.
2. Telegram Desktop [does not support](https://github.com/telegramdesktop/tdesktop/issues/5795) rich format text copy & paste. It can do only plain text. So you can't copy a pretty formatted text from a web page or a rich text editor.
3. The layout of a post slightly differs between the blog and the channel.
4. Post scheduling using the script is quicker.
5. Telegram bots [don't have](https://core.telegram.org/bots/api#sendmessage) a schedule option.
