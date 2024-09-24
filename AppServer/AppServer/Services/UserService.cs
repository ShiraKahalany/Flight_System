using AppServer.Data;
using AppServer.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

public interface IUserService
{
    Task AddUserAsync(User user);
    Task DeleteUserAsync(int id);
    Task<User?> GetUserByIdAsync(int id);
    Task<List<User>> GetAllUsersAsync();
    Task DeleteAllUsersAsync();
    Task<User?> GetUserByUsernameAndPasswordAsync(string username, string password);
    Task<User?> GetUserByUsernameAsync(string username); // New method to check for duplicate usernames
}

public class UserService : IUserService
{
    private readonly DBContext _context;

    public UserService(DBContext context)
    {
        _context = context;
    }

    // Add a new user
    public async Task AddUserAsync(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
    }

    // Delete a user by its Id
    public async Task DeleteUserAsync(int id)
    {
        var user = await _context.Users.FindAsync(id);
        if (user == null)
        {
            throw new KeyNotFoundException("User not found.");
        }
        _context.Users.Remove(user);
        await _context.SaveChangesAsync();
    }

    // Delete all users
    public async Task DeleteAllUsersAsync()
    {
        var users = await _context.Users.ToListAsync();
        _context.Users.RemoveRange(users);
        await _context.SaveChangesAsync();
    }

    // Get a user by its Id
    public async Task<User?> GetUserByIdAsync(int id)
    {
        return await _context.Users.FindAsync(id);
    }

    // Get all users
    public async Task<List<User>> GetAllUsersAsync()
    {
        return await _context.Users.ToListAsync();
    }

    // Get a user by username and password
    public async Task<User?> GetUserByUsernameAndPasswordAsync(string username, string password)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Username == username && u.Password == password);
    }

    // Get a user by username (to check for duplicates)
    public async Task<User?> GetUserByUsernameAsync(string username)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Username == username);
    }
}
