const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');

const User = sequelize.define('User', {
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  name: DataTypes.STRING,
  email: { type: DataTypes.STRING, unique: true },
  password: DataTypes.STRING,
  privacySettings: {
    type: DataTypes.JSON,   // Ex: {profileVisibility: 'friends', contactInfo: 'private'}
    defaultValue: {}
  }
});

module.exports = User;