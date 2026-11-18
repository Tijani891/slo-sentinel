"""Cloudflare Worker entrypoint.

Only this file imports Workers-runtime modules. Keep it thin: it adapts the
runtime's fetch (and, from day 10, scheduled) events onto code in the
`slo_sentinel` package, which is tested under plain CPython.
"""

from workers import WorkerEntrypoint

from slo_sentinel.app import app


class Default(WorkerEntrypoint):
    async def fetch(self, request):  # type: ignore[no-untyped-def]
        import asgi  # provided by the Workers runtime

        return await asgi.fetch(app, request.js_object, self.env)