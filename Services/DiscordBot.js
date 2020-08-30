const {
  name,
  token,
  oID,
  prefix,
  version,
} = require('../config.json');
const Discord = require('discord.js');
const client = new Discord.Client();
const auddit = require('./Auddit.js');

//const command = require('./CommandHandler.js');
//const currency = require('./CurrencyHandler.js');

client.login(token);

client.once('ready', () => {
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
  command.execute(message);
});

//When a messageDelete
client.on('messageDelete', async message => {
  auddit.deleted(client, message);
});

module.exports = { client }
