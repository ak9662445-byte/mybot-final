export default {
  async fetch(request) {
    return new Response("mybot-final Cloudflare Worker is online!", {
      status: 200,
      headers: {
        "content-type": "text/plain; charset=UTF-8"
      }
    });
  }
};
