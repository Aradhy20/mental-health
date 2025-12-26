const request = require('supertest');
const app = require('../server');
const mongoose = require('mongoose');
const User = require('../models/User');

let token;
let server;

beforeAll(async () => {
    // Connect to a test database or use a separate DB
    // For this quick check, we'll assume the main DB is fine or use a mock
    // TO KEEP IT SAFE: We won't wipe the DB, just create a unique user
    server = app.listen(5001); // Use different port for testing
});

afterAll(async () => {
    await mongoose.connection.close();
    server.close();
});

describe('MERN API Integrity Test', () => {
    it('GET /health - should return 200 and healthy status', async () => {
        const res = await request(app).get('/health');
        expect(res.statusCode).toEqual(200);
        expect(res.body.stack).toEqual('MERN');
    });

    it('POST /api/auth/register - should create a new user', async () => {
        const uniqueUser = `testUser_${Date.now()}`;
        const res = await request(app)
            .post('/api/auth/register')
            .send({
                name: 'Test Runner',
                email: `${uniqueUser}@example.com`,
                password: 'password123',
                username: uniqueUser
            });

        expect(res.statusCode).toEqual(200);
        expect(res.body).toHaveProperty('token');
        token = res.body.token;
    });

    it('GET /api/users/me - should return user profile', async () => {
        const res = await request(app)
            .get('/api/users/me')
            .set('Authorization', `Bearer ${token}`);

        expect(res.statusCode).toEqual(200);
        expect(res.body).toHaveProperty('email');
    });

    it('POST /api/mood - should log a mood', async () => {
        const res = await request(app)
            .post('/api/mood')
            .set('Authorization', `Bearer ${token}`)
            .send({
                score: 8,
                label: 'Happy',
                note: 'Testing from Jest'
            });

        expect(res.statusCode).toEqual(200);
        expect(res.body.label).toEqual('Happy');
    });
});
