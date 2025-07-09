# Use Ruby as the base image
# It's a Debian based image
FROM ruby:3.1.2 # supports multi-architecture (multi-arch) builds, meaning it works natively on both Intel and ARM platforms (Zorin OS & Asahi)

# Install dependencies
RUN apt-get update && apt-get install -y build-essential nodejs

# Install Bundler
RUN gem install bundler:2.5.18

# Set the working directory
WORKDIR /app

# Copy the Gemfile and Gemfile.lock, they should be in the same dir as this file
COPY Gemfile Gemfile.lock ./

# Install Jekyll and other dependencies
RUN bundle install

# Copy the rest of the application
# Copy all files and directories from the build context (usually the directory containing the Dockerfile) into the current working directory in the Docker image.
COPY . .

# Ensure the _site directory is not being served (if it exists from previous runs)
RUN rm -rf _site

# Expose port 4000 (Jekyll's default port)
# It's a way to communicate which ports are intended to be published
# To actually make the port accessible when running the container, you need to use the -p flag with docker run, as we did earlier with -p 4000:4000
EXPOSE 4000

# Start Jekyll server
# CMD [] specifies the command that should be run when the container starts
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]
