export const queue = {
  async enqueue(topic: string, payload: any) {
    console.log('Enqueued', topic, payload);
    // Plug in BullMQ / RabbitMQ / Cloud Tasks here
  }
};
