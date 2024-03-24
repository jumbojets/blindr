# Wordle in the zkVM

## Quick Start

First, follow the [examples guide] to install dependencies and check out the correct version of the example.

Then, run the example with:

```bash
cargo run --release
```

Welcome to Wordle! Start guessing 5 letter words!

[examples guide]: https://dev.risczero.com/api/zkvm/examples/#running-the-examples

## About the game

The [game](src/main.rs) consists of two agents: a player and a server.
The zkVM enforces that the server plays fairly.

The game begins with the server choosing a secret word from the [wordlist](src/wordlist.rs), and sending the player the hash of the secret word.

The player then submits guesses. After each guess, the server returns which letters from the guess match the letters in the secret word.
In addition, the server returns a [receipt](https://www.risczero.com/docs/explainers/proof-system/) that attests to the logic of the letter-checking and [includes the hash](methods/guest/src/main.rs) of the secret word.

## Ensuring fair play

The player ensures that server isn't cheating using the [`check_receipt` function](src/main.rs).
This function first runs `receipt.verify(WORDLE_ID)` which ensures that the receipt is valid and was generated by the correct binary file.
Then, the `check_receipt` function checks that the hash in the [journal contents](https://www.risczero.com/docs/explainers/zkvm/) match the hash of the secret word provided at the start of the game.