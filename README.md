# docs/
*Website for my course material: [https://www.meneermaes.be/](https://www.meneermaes.be/)*

# Setup
1. Install dependencies: `gem install jekyll bundler`
2. Navigate to the dir containing the Gemfile
3. Install gems listed in the Gemfile: `bundle install`

## Setup errors & fixes
**You don't have /home/hanne/bin in your PATH, gem executables will not run.**
- Cause: the directory /home/hanne/bin is not included in your PATH, which means that any executables installed by Ruby gems (such as jekyll) may not be found when you try to run them
- Fix: add this line to .bashrc: `export PATH="$HOME/bin:$PATH"`

# maesbot/
*Tooling to make my life easier*

**maesbot/diff-file**
![diff-fileTerminal output](readme/carbon.png)

**maesbot/punten/**
Automate everything that involves points, assignements, tests, ...
