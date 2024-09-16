# docs/
*Website for my course material: [https://www.meneermaes.be/](https://www.meneermaes.be/)*

## Setup
1. Install ruby gems:
    - Ubuntu: `sudo apt install ruby-rubygems`
2. Install dependencies: `sudo gem install jekyll bundler`
    *Bundler is a dependency manager that will use your Gemfile to install and manage gem versions.*
3. Navigate to the dir containing the Gemfile
4. Install gems listed in the Gemfile: `bundle install`
    *Reads the Gemfile, downloads and installs the gems and their dependencies, creates a Gemfile.lock file that records the exact versions of every gem installed*

### Setup errors & fixes

**You don't have /home/hanne/bin in your PATH, gem executables will not run.**
- **Cause:** the directory /home/hanne/bin is not included in your PATH, which means that any executables installed by Ruby gems (such as jekyll) may not be found when you try to run them
- **Fix:** add this line to .bashrc: `export PATH="$HOME/bin:$PATH"`

**An error occurred while installing http_parser.rb (0.8.0), and Bundler cannot continue.**
- Install dependencies: `sudo apt-get install build-essential patch ruby-dev zlib1g-dev liblzma-dev`

**An error occurred while installing rake (13.2.1), and Bundler cannot continue.**
1. gem install bundler
2. rm -rf Gemfile.lock
3. bundle install
4. gem install rake
5. sudo bundle install

# maesbot/
*Tooling to make my life easier*

**maesbot/diff-file**
![diff-fileTerminal output](readme/carbon.png)

**maesbot/punten/**
Automate everything that involves points, assignements, tests, ...

# System agnostic
*I try to make everything system agnostic (Jekyll especially, it was giving me errors after every sync between computers)*

- Always use `bundle exec` when running Jekyll commands.
    *Bundler is a dependency management tool for Ruby projects. It helps manage the gems (Ruby libraries) that your project depends on.*
- .gitignore Jelyll stuff
