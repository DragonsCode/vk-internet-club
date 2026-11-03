# vk-internet-club
VK internet club


## Secret configuration

Set `VK_BOT_TOKEN` in the process environment before starting. Each is required; missing or blank values stop startup without printing credentials. `.env.example` lists the names only. The application does not automatically load `.env`; export the variables in your shell or configure your service/container environment. Never commit real values.

Credentials previously committed to this repository must be revoked or rotated in the relevant provider or deployment. Removing them from current source does not remove Git history; assess historical exposure separately. No live credentials are needed for the offline configuration tests:

```sh
python -m unittest discover -s tests -v
```
