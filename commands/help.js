const {
  prefix
} = require('../config.json');
const client = require('../Services/DiscordBot.js');
module.exports = {
  name: 'help',
  description: 'List all of my commands or info about a specific command.',
  aliases: ['commands'],
  usage: 'help <command>',
  cooldown: 5,
  execute(message, args) {
    const data = [];
    const { commands } = client;

    //console.log(commands);
    if (!args.length) {
      data.push('Here\'s a list of all my commands:');
      data.push(commands.map(command => '`' + command.name + '`').join(', '));
      data.push(`\nYou can send \`${prefix}help [command name]\` to get info on a specific command!`);

      return message.author.send(data, {
          split: true
        })
        .then(() => {
          if (message.channel.type === 'dm') return;
          message.reply('I\'ve sent you a DM with all my commands!');
        })
        .catch(error => {
          console.error(`Could not send help DM to ${message.author.tag}.\n`, error);
          message.reply('it seems like I can\'t DM you! Do you have DMs disabled?');
        });
    }
    const name = args[0].toLowerCase();
    const command = commands.get(name) || commands.find(c => c.aliases && c.aliases.includes(name));

    if (!command) {
      return message.reply('that\'s not a valid command!');
    }

    data.push(`> **Name:** \n${command.name}`);

    if (command.aliases) data.push(`> **Aliases:** \n${command.aliases.join(', ')}`);
    if (command.description) data.push(`> **Description:** \n ${command.description}`);
    if (command.usage) data.push(`> **Usage:** \n\`${prefix}${command.name} ${command.usage}\``);

    data.push(`> **Cooldown:** \n${command.cooldown || 3} second(s)`);

    message.channel.send(data, {
      split: true
    });

    // ...
  },
};
