#Unity EC2 Info Lens##

##Why##

I created this lens to have a way to quickly access several EC2 instances running across several accounts. I am a freelance developer and many of my clients have servers/applications on EC2. Normally the IP addresses of each instance changes when the AMI launches. This is quite normal and easy to get around. However because I have many clients with many servers each, it can be a pain to track down the current public IP address of a server that is having a problem. 

[Elastics](http://tundrabot.com/elastics) on OS X used to over this nicely. However, there is not equivalent available on Linux.

##How to Use##
First install [The AWS command line tool](http://www.timkay.com/aws/). This lens uses it to gain access to the data.

Second install the deb package or use the source (it's using the quickly template tool, but I don't like BZR so .....)

Next create files in ~/.ec2-info/ that have two lines. The first is the access id the second is the access key. The [The AWS  tool page](http://www.timkay.com/aws/) has a good example. Remeber this lens uses it to fetch data.

That's it, your good to go. It could take up to 5 mins. to get your first set of hosts, or your could: 

    setsid unity

to speed it up.

##Important Notes##

1. I am not a python developer. This code works, but is not awesome. It needs lots of clean up, and I did some things that got it working that could have been done better.
2. I use this lens. That is good enough for me. I am posting it here, so that others can use it, as an example, or if they get it working, then as a lens. I have little intention of adding features, though you may contact me, and if I think there useful I will add them.