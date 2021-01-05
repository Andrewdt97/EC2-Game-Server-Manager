# EC2 Game Server Manager
### By Andrew Thomas

## Motivation
In the early (and current) days of the pandemic, my friends and I turned to weekly Minecraft sessions to stay connected. Having recently covered the basics of AWS, I wanted a more significant project to tune my skills as well as a way to take advantage of the relatively low-cost of EC2 rent for our gaming sessions. Thus, this project was born. The main goal was to allow pseudo 24-hour uptime. We only played a couple hours per week, so paying for 24/7 service was a waste, but I wanted others to be able to use the server even when I was unavailable.

## Solution Overview
At its most basic level, the solution is able to launch EC2 instances from templates and shut them down via a web app and API. It was originally designed for Minecraft servers, but can easily be configured for much more. 

### Django API
The `api` folder contains a Django project designed to be deployed to Elastic Beanstalk. The `api/config/servers.json` contains the EC2 templates that can be launched. Upon receiving a call to shutdown the EC2 instance, the server connects to the instance via ssh and looks for a `shutdown.sh` script to execute.

### React App
The basic React web app can be deployed as a static site to an S3 bucket for easy hosting. It will display the IP address of a running EC2 instance as well as making calls to start and stop the server.

## Deployment
Current deployment requires basic knowledge of Django, React, and AWS (EB, EC2, S3). I hope to be able to provide more detailed and user-friendly deployment in the near future.

### AWS
1. Create a EC2 template which includes a deployment of a script called `shutdown.sh` that governs shutdown behavior
2. Create an EB environment

### Django
1. Update `api\proj_config.py` to your configuration
2. Set all environment variables listed in `api\proj_config.py`

### React
1. Set `productionHostname` and `productionApiHostname` in `config/api-config.js`
2. Deploy to public S3 bucket

## Future Improvements
This project, while functional, is far from complete. Here are some ideas for improvement in no particular order.

- Update code to include more best practices (I have already identified a lot of sloppy code)
- Add users and permissions instead of simple password security
- Write some css for the web app
- Automatically shutdown the EC2 instance if empty for ~5 minutes
- Write full tutorial for deploying minecraft server
- Deployment scripts
