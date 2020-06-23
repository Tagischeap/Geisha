module.exports = {
  name: 'poll',
  aliases: ['vote', 'v', 'p'],
  description: 'Makes a poll.',
  args: true,
  usage: 'poll <Question>, <option 1>, <option 2>...',
  execute(message, args) {
    const fArg = message.content.substr(message.content.indexOf(' ') + 1);

    var input = fArg.split(',');
    var pollText = input[0] + "";
    if (input.length > 1) {
      for (var i = 1; i < input.length; i++) {
        if (i > 10)
          return;
        if (i === 1)
          pollText += '\n1️⃣ ';
        if (i === 2)
          pollText += '\n2️⃣ ';
        if (i === 3)
          pollText += '\n3️⃣ ';
        if (i === 4)
          pollText += '\n4️⃣ ';
        if (i === 5)
          pollText += '\n5️⃣ ';
        if (i === 6)
          pollText += '\n6️⃣ ';
        if (i === 7)
          pollText += '\n7️⃣ ';
        if (i === 8)
          pollText += '\n8️⃣ ';
        if (i === 9)
          pollText += '\n9️⃣ ';
        if (i === 10)
          pollText += '\n🔟 ';

        pollText += input[i];
      }
    }
    try {
      message.channel.send(pollText).then((pollMessage) => {
        if (args.length > 1) {
          for (var i = 1; i < input.length; i++) {
            if (i > 10)
              return;
            if (i === 1)
              pollMessage.react('1️⃣');
            if (i === 2)
              pollMessage.react('2️⃣');
            if (i === 3)
              pollMessage.react('3️⃣');
            if (i === 4)
              pollMessage.react('4️⃣');
            if (i === 5)
              pollMessage.react('5️⃣');
            if (i === 6)
              pollMessage.react('6️⃣');
            if (i === 7)
              pollMessage.react('7️⃣');
            if (i === 8)
              pollMessage.react('8️⃣');
            if (i === 9)
              pollMessage.react('9️⃣');
            if (i === 10)
              pollMessage.react('🔟');
          }
        }
        else {
          pollMessage.react('🇴');
          pollMessage.react('🇽');
        }
      });

      if (message.member.permissions.has('MANAGE_MESSAGES')) {
        //message.delete({ timeout: 5000, reason: 'For poll' });
      }
    }
    catch (error) {
      console.error(error);
    }
  },
};
