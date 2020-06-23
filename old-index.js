const fs = require('fs');
const Discord = require('discord.js');
const {
  name,
  token,
  oID,
  prefix,
  version,
} = require('./config.json');
const client = new Discord.Client();

// Collecting commands
client.commands = new Discord.Collection();

console.log('Finding commands...');
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
  const command = require(`./commands/${file}`);
  console.log(`\n ${command.name} found.`);
  // set a new item in the Collection
  // with the key as the command name and the value as the exported module
  client.commands.set(command.name, command);
}
const cooldowns = new Discord.Collection();

// When bot starts
client.on('ready', async () => {
  console.log(
    '\n----------------------------------------------------------------' +
    `\nLogged in as ${client.user.tag}! ` +
    '\nApplication: ' + name +
    '\nOwnerID: ' + oID +
    '\nVersion: ' + version +
    '\nPrefix: ' + prefix +
    '\n----------------------------------------------------------------\n'
  );

  client.user.setActivity('you. (' + version + ')', { type: 'WATCHING' });
});
// When a message is sent
client.on('message', async message => {
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

});
//When a messageDelete
client.on('messageDelete', async message => {

	// ignore direct messages
	if (!message.guild) return;
  if(message.content.startsWith(prefix) || message.author.bot) return;

	const fetchedLogs = await message.guild.fetchAuditLogs({
		limit: 1,
		type: 'MESSAGE_DELETE',
	});
	// Since we only have 1 audit log entry in this collection, we can simply grab the first one
	const deletionLog = fetchedLogs.entries.first();

  const delchannel = client.channels.cache.get('699115417406406656');

	// Let's perform a sanity check here and make sure we got *something*
	if (!deletionLog) return console.log(`A message by ${message.author.tag} was deleted, but no relevant audit logs were found.`);

	// We now grab the user object of the person who deleted the message
	// Let us also grab the target of this action to double check things
	const { executor, target } = deletionLog;


	// And now we can update our output with a bit more information
	// We will also run a check to make sure the log we got was for the same author's message
	if (target.id === message.author.id) {
    let embed = new Discord.MessageEmbed()
      .setTitle("**DELETED MESSAGE**")
      .setColor("#fc3c3c")
      .setAuthor(message.author.tag, message.author.avatarURL)
      .setDescription(`**Author:** ${message.author.tag}\n**Channel:** ${message.channel}\n**Message:** ${message.content}\n**Executor**: ${executor.tag}`)
      .setFooter(`Message ID: ${message.id}\nAuthor ID: ${message.author.id}`)
      .setThumbnail(message.author.avatarURL)
      .setTimestamp();
    try {
      delchannel.send(embed);
    } catch (error) {
        console.error(error);
    }
	}	else {
    let embed = new Discord.MessageEmbed()
      .setTitle("**DELETED MESSAGE**")
      .setColor("#fc3c3c")
      .setAuthor(message.author.tag, message.author.avatarURL)
      .setDescription(`**Author:** ${message.author.tag}\n**Channel:** ${message.channel}\n**Message:** ${message.content}`)
      .setFooter(`Message ID: ${message.id}\nAuthor ID: ${message.author.id}`)
      .setThumbnail(message.author.avatarURL)
      .setTimestamp();
    try {
      delchannel.send(embed);
    } catch (error) {
        console.error(error);
    }
	}
});

client.login(token);
