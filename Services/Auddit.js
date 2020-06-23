const {
  name,
  token,
  oID,
  prefix,
  version,
} = require('../config.json');
const Discord = require('discord.js');
//const client = require('./DiscordBot.js');


var Auddit = function() {

}

this.messaged = async function(message)
{
  // TODO
}

this.deleted = async function(client, message)
{
  console.log(message);
  	// ignore direct messages
  	if (!message.guild) return;
    //If message is bot message message starts with prefix
    //if(message.content.startsWith(prefix) || message.author.bot) return;

  	const fetchedLogs = await message.guild.fetchAuditLogs({
  		limit: 1,
  		type: 'MESSAGE_DELETE',
  	});
  	// Since we only have 1 audit log entry in this collection, we can simply grab the first one
  	const deletionLog = fetchedLogs.entries.first();

    const delchannel = client.channels.cache.get('699115417406406656');

  	// Let's perform a sanity check here and make sure we got *something*
  	if (!deletionLog) return console.log(`A message by ${message.author.tag}`
      + ` was deleted, but no relevant audit logs were found.`);

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
        .setDescription(`**Author:** ${message.author.tag}`
          + `\n**Channel:** ${message.channel}`
          + `\n**Message:** ${message.content}`
          + `\n**Executor**: ${executor.tag}`)
        .setFooter(`Message ID: ${message.id}`
          + `\nAuthor ID: ${message.author.id}`)
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
        .setDescription(`**Author:** ${message.author.tag}`
          + `\n**Channel:** ${message.channel}`
          + `\n**Message:** ${message.content}`)
        .setFooter(`Message ID: ${message.id}`
          + `\nAuthor ID: ${message.author.id}`)
        .setThumbnail(message.author.avatarURL)
        .setTimestamp();
      try {
        delchannel.send(embed);
      } catch (error) {
          console.error(error);
      }
  	}
}
