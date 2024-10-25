const {
  name,
  token,
  oID,
  prefix,
  version,
} = require('../config.json');
const Discord = require('discord.js');
const client = require('./DiscordBot.js');
const fs = require('fs');

// Collecting commands
console.log('\n\nFinding commands...\n');

client.commands = new Discord.Collection();
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
  const command = require(`../commands/${file}`);
  console.log(`${command.name} found.`);
  // set a new item in the Collection
  // with the key as the command name and the value as the exported module
  client.commands.set(command.name, command);
}
const cooldowns = new Discord.Collection();

var CommandHandler = function() {
  console.log('\n\nCommand Handler...\n');
}

this.execute = function(message) {
  //currency.add(message.author.id, 1);

  if (!message.content.startsWith(prefix) || message.author.bot) return;

  const args = message.content.slice(prefix.length).split(/ +/);
  const commandName = args.shift().toLowerCase();

  const command = client.commands.get(commandName) ||
    client.commands.find(cmd => cmd.aliases && cmd.aliases.includes(commandName));
  if (!command) return;
  if (command.guildOnly && message.channel.type !== 'text') {
    return message.reply('I can\'t execute that command inside DMs!');
  }
  if (command.args && !args.length) {
    let reply = `You didn't provide any arguments, ${message.author}!`;
    if (command.usage) {
      reply += `\nThe proper usage would be: \`${prefix}${command.name} ${command.usage}\``;
    }
    return message.channel.send(reply);
    // return message.react('👀');
  }
  if (!cooldowns.has(command.name)) {
    cooldowns.set(command.name, new Discord.Collection());
  }

  const now = Date.now();
  const timestamps = cooldowns.get(command.name);
  const cooldownAmount = (command.cooldown || 3) * 1000;

  if (timestamps.has(message.author.id)) {
    const expirationTime = timestamps.get(message.author.id) + cooldownAmount;
    if (now < expirationTime) {
      const timeLeft = (expirationTime - now) / 1000;
      // return message.reply(`Please slow down you're going too fast! 💦 \n(${timeLeft.toFixed(1)} more second(s) you can reusing the \`${command.name}\` command.)`);
      return message.react('💦');
    }
  }

  timestamps.set(message.author.id, now);
  setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);
  try {
    command.execute(message, args);
  }
  catch (error) {
    console.error(error);
    message.react('👀');
  }
}
