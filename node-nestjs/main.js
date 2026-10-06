// Plain JavaScript (no TypeScript build step) using Nest's programmatic API instead of decorators.
require('reflect-metadata');
const { NestFactory } = require('@nestjs/core');
const { Module, Controller, Get, Param, BadRequestException } = require('@nestjs/common');

class OrdersController {
  health() {
    return { status: 'UP' };
  }

  order(idParam) {
    const id = Number(idParam);
    if (!Number.isInteger(id) || id < 0) throw new BadRequestException('bad id');
    return { id, customer: `c-${id % 100}`, total: (id % 1000) + 0.5, status: 'NEW' };
  }
}

// Decorators applied by hand so the file runs on plain Node.
Controller()(OrdersController);
const proto = OrdersController.prototype;
Get('health')(proto, 'health', Object.getOwnPropertyDescriptor(proto, 'health'));
Get('orders/:id')(proto, 'order', Object.getOwnPropertyDescriptor(proto, 'order'));
Param('id')(proto, 'order', 0);

class AppModule {}
Module({ controllers: [OrdersController] })(AppModule);

NestFactory.create(AppModule, { logger: ['error'] }).then((app) => app.listen(process.env.PORT || 8080));
