---
Title: Personal News Analysis
summary: Automatically find relevant news from the Web.
---

Systematically retrieves online news articles, enriches them, scans them for keywords and sends hits to [GetPocket.com](https://getpocket.com/). All analysis components are loosely-coupled with [NATS.io](https://nats.io/) work queues, which also allows scaling single-core-CPU-intensive components easily.



![](architecture.drawio.svg)

[Open In Draw.io](https://app.diagrams.net/?url=https://raw.githubusercontent.com/heussd/nats-news-analysis/main/architecture.drawio)


## Involved services

All services are orchestrated and scaled with `docker-compose.yml`.

### Custom services

- [ghcr.io/heussd/nats-news-analysis/rss-article-url-feeder-python](https://ghcr.io/heussd/nats-news-analysis/rss-article-url-feeder-python) - Feeds news articles from RSS feeds.
- [ghcr.io/heussd/nats-news-analysis/rss-article-url-feeder-go](https://ghcr.io/heussd/nats-news-analysis/rss-article-url-feeder-go) - Feeds news articles from RSS feeds (Go re-implementation).
- [ghcr.io/heussd/nats-news-analysis/keyword-matcher-python](https://ghcr.io/heussd/nats-news-analysis/keyword-matcher-python) - Matches against keywords list.
- [ghcr.io/heussd/nats-news-analysis/keyword-matcher-go](https://ghcr.io/heussd/nats-news-analysis/keyword-matcher-go) - Matches against keywords list (Go re-implementation).
- [ghcr.io/heussd/nats-news-analysis/pocket-integration](https://ghcr.io/heussd/nats-news-analysis/pocket-integration) - Feeds matches into getpocket.com.
- [docker.io/heussd/fivefilters-full-text-rss](https://hub.docker.com/r/heussd/fivefilters-full-text-rss) - Retrieves full text of web pages.


### Third party services

- [docker.io/nats](https://hub.docker.com/_/nats) - Event queue, key-value store and deduplication.
- [NGINX](https://www.nginx.com/) - Simple load balancer / reverse proxy
- [getpocket.com API](https://getpocket.com/developer/) - "Read it later" online service.

## Message queue for scaling

Instead of blocking the application with a single core keyword matching operation, or even trying to build a complex multi-threading keyword matching, we are using the `scale` option of docker compose to run multiple single-core keyword matching components in parallel, wired together with the message queue. This allows us to keep individual components super straight-forward and easy to maintain.


### Keyword matching containers, scaled up

![](docker-container.png)


### One core per keyword matching

![](cpu-cores.png)
