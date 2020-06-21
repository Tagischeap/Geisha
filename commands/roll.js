module.exports = {
  name: 'roll',
  aliases: ['r', 'math', 'm', 'sum', 'solve', 'quickmaths', 'qm'],
  description: 'Rolls dice with basic algebra syntax.' +
    '\n\n `d6` will roll a single six sided die.' +
    '\n `4d20` will roll four twenty sided dice.' +
    '\n `1d6!` will make the roll exploading.' +
    '\n - An exploding die is rolled again whenever its highest value is rolled.' +
    'The rolled values are summed' +
    '\n\n Operators can be added to roll addtional dice or moddify it\'s result.' +
    '\n Try `4d8! * 5 + d4^3d8! / (d6 + 5 - 2d4)`',
  usage: '1d6',
  cooldown: 5,
  execute(message, args) {
    const fArg = message.content.substr(message.content.indexOf(' ') + 1);
    // Dice rolling
    const equation = fArg.replace(/\s/g, ' ');
    const dicePattern = /\d*d\d+!?/g;
    const diceExtract = /(\d*)d(\d+)(!?)/;
    const maxAmmo = 201;
    const maxSize = 9001;
    let roller = equation.match(dicePattern);
    if (roller === null) {
      roller = [];
    }
    let rollOutput = equation;
    let mathString = equation;
    let rollString = '';
    let roll = 0;
    let broke = false;
    // console.log(roller);
/*
    if (roller.length > 0) {
*/
      // Start Rolling
      roller.forEach(function(element) {
        const extraction = element.match(diceExtract);
        let ammount = parseInt(extraction[1], 10);
        if (isNaN(ammount)) {
          ammount = 1;
        }
        const size = parseInt(extraction[2], 10);
        const exploading = extraction[3];
        let exploadcount = 0;
        let exploadsize = 0;
        roll = 0;
        rollString = '';

        // console.log(ammount + 'd' + size + '' + exploading);

        if (ammount <= maxAmmo && size <= maxSize && size > 1) {
          // Rolls each die
          rollString += '(';
          for (let i = 0; i < ammount; i++) {
            const n = Math.floor((Math.random() * size) + 1);
            // If the dice exploaded
            if (n === size && exploading === '!') {
              // console.log(n + ' exploaded');
              if (exploadcount == 0) {
                // Starting explotion
                rollString += '';
              }
              i--;
              exploadcount++;
              roll += n;
              exploadsize += n;
            }
            else if (n != size && exploadcount > 0) {
              roll += n;
              exploadsize += n;
              rollString += exploadsize.toString();
              // Ending explotion
              rollString += '';
              rollString += '!'.repeat(exploadcount);
              if (i < ammount - 1) {
                rollString += ' + ';
              }
              // console.log(roll + ' ' + exploadcount + ' ' + exploadsize);
              exploadcount = 0;
              exploadsize = 0;
            }
            else {
              // Rembering rolls
              roll += n;
              rollString += n.toString();
              if (i < ammount - 1) {
                rollString += ' + ';
              }
            }
          }
          rollString += ')';
        }
        // Trying to break it
        else if (size < 1) {
          mathString = '\n> 🎲 You rolled: **∞**';
          broke = true;
          return false;
        }
        // Too many dice
        else if (ammount > maxAmmo || size > maxSize) {
          mathString = 'That\'s too big for me to handle.';
          broke = true;
          return false;
        }
        else {
          if (Math.floor((Math.random() * 2) + 1) > 2){
            mathString = 'Your notation doesn\'t make sense.';
          }
          else {
            mathString = '*Rolls on floor*';
          }
          broke = true;
          return false;
        }
        // Changes strings to be dice roll results.
        if (!broke) {
          mathString = mathString.replace(diceExtract, roll);
          rollOutput = rollOutput.replace(diceExtract, rollString);
        }
      });
      // console.log('math: ' + mathString);
      // console.log('outp: ' + rollOutput);
      // console.log('----');

      // Result
      try {
        mathString = eval(mathString);
      }
      catch (err) {
        rollOutput += '\n---\n' + err;
      }
      if (!broke && (roller.length > 1 || parseInt(roller[0].match(diceExtract)[1]) > 1)) {
        message.reply('\n>>> 🎲 You rolled: ' + mathString + '\n```js\n' + rollOutput + '```');
      }
      // Single result
      else if (!broke) {
        message.reply('\n> 🎲 You rolled: ' + mathString);
      }
      // error output
      else {
        message.reply(mathString);
      }

    /*
    }
    else {
      // TODO: quick d6 roll.
      message.channel.send('*Rolls on floor*\n``' + equation + '``');
    }
    */
  },
};

function rollTheDice(size, ammount) {
  // TODO
}
