# anchore-proxy
## about this project
This is a really simple proxy for that I wrote that will reissue requests that are sent to the **/get** and **/post** URL paths. Currently this proxy is not secure, but I will be making a configuration that will make it more secure so that it isn't just an open proxy.

## dependencies

This image has no dependencies other than the ones specified in the **requirements.txt** file.

## building

To build the image, simply run a **docker build** command like so:

```
docker build -t anchore-proxy:latest .
```

## usage

You can run this image independently by simply issuing this command:

```
docker run -p5000:5000 anchore-proxy
```

If you want to run it in the background, add a **-d** flag:

```
docker run -d -p5000:5000 anchore-proxy
```

## api

The proxy listens on port 5000. You can remap that from the command line using the **-p** argument of **docker run**. Eventually I will make this more configurable. There are two main request URLs.

```
GET 'http://localhost:5000/get?target=https://xyz.com&headers={"Content-Type": "text/plain"}'
POST 'http://locahost:5000/post?target=https://xzy.com&headers={"Content-Type": "application/json"}'
```

#### params

* **target** - the target URL, including query params. Should be URL encoded as necessary
* **headers** - optional headers that should be passed along, encoded as json
