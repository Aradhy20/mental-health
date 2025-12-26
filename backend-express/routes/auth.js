const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Helper function to generate 6-digit OTP
const generateOTP = () => Math.floor(100000 + Math.random() * 900000).toString();

// @route   POST api/auth/register
// @desc    Register user
// @access  Public
router.post('/register', async (req, res) => {
    try {
        const { username, email, password, full_name, phone } = req.body;

        // MongoDB Path
        let userByEmail = await User.findOne({ email });
        if (userByEmail) return res.status(400).json({ message: 'Email already registered' });

        if (phone) {
            let userByPhone = await User.findOne({ phone });
            if (userByPhone) return res.status(400).json({ message: 'Phone number already registered' });
        }

        const user = new User({ username, email, password, full_name, phone });
        await user.save();

        const payload = { user: { id: user.id } };
        jwt.sign(payload, process.env.JWT_SECRET || 'secret', { expiresIn: '7d' }, (err, token) => {
            if (err) throw err;
            res.json({ token, user: { id: user.id, username, email, full_name, phone } });
        });
    } catch (err) {
        console.error('Registration Error:', err.message);
        res.status(500).json({ message: 'Auth Engine Failure', error: err.message });
    }
});

// @route   POST api/auth/login
// @desc    Authenticate user via Email & Password
// @access  Public
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        const user = await User.findOne({ email }).select('+password');
        if (!user) return res.status(400).json({ message: 'Invalid Credentials' });

        const isMatch = await user.comparePassword(password);
        if (!isMatch) return res.status(400).json({ message: 'Invalid Credentials' });

        const payload = { user: { id: user.id } };
        jwt.sign(payload, process.env.JWT_SECRET || 'secret', { expiresIn: '7d' }, (err, token) => {
            if (err) throw err;
            res.json({ token, user: { id: user.id, username: user.username, email: user.email, full_name: user.full_name, phone: user.phone } });
        });
    } catch (err) {
        console.error('Login Error:', err.message);
        res.status(500).json({ message: 'Auth Engine Failure' });
    }
});

// @route   POST api/auth/request-otp
// @desc    Generate and "send" OTP to mobile number
// @access  Public
router.post('/request-otp', async (req, res) => {
    try {
        let { phone } = req.body;
        if (!phone) return res.status(400).json({ message: 'Phone number required' });

        phone = phone.trim();
        const otp = generateOTP();

        let user = await User.findOne({ phone });
        if (!user) return res.status(404).json({ message: 'No account found for this phone' });

        user.otp = otp;
        user.otpExpires = new Date(Date.now() + 10 * 60 * 1000);
        await user.save();

        console.log(`[AUTH-DEBUG] OTP for ${phone}: ${otp}`);
        res.json({ message: 'OTP sent successfully', debug_otp: otp });
    } catch (err) {
        console.error('OTP Request Error:', err.message);
        res.status(500).json({ message: 'Auth Engine Failure' });
    }
});

// @route   POST api/auth/verify-otp
// @desc    Verify OTP and login
// @access  Public
router.post('/verify-otp', async (req, res) => {
    try {
        let { phone, otp } = req.body;
        if (!phone || !otp) return res.status(400).json({ message: 'Phone and OTP required' });

        phone = phone.trim();

        let user = await User.findOne({ phone, otp, otpExpires: { $gt: new Date() } });
        if (!user) return res.status(400).json({ message: 'Invalid or expired OTP' });

        user.otp = null;
        user.otpExpires = null;
        await user.save();

        const payload = { user: { id: user.id } };
        jwt.sign(payload, process.env.JWT_SECRET || 'secret', { expiresIn: '7d' }, (err, token) => {
            if (err) throw err;
            res.json({ token, user: { id: user.id, username: user.username, email: user.email, full_name: user.full_name, phone: user.phone } });
        });
    } catch (err) {
        console.error('OTP Verify Error:', err.message);
        res.status(500).json({ message: 'Auth Engine Failure' });
    }
});

module.exports = router;
