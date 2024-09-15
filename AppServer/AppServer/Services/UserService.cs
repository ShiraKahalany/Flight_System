using AppServer.Data;
using AppServer.Models;
using Microsoft.EntityFrameworkCore;


public interface IUserService
{
    Task AddUserAsync(User user);
    Task DeleteUserAsync(int id);
    Task<User> GetUserByIdAsync(int id);
    Task<List<User>> GetAllUsersAsync();
    Task DeleteAllUsersAsync(); 
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
        if (user != null)
        {
            _context.Users.Remove(user);
            await _context.SaveChangesAsync();
        }
    }
    //delete all users
    public async Task DeleteAllUsersAsync()
    {
        var users = _context.Users.ToList();
        _context.Users.RemoveRange(users);
        await _context.SaveChangesAsync();
    }

    // Get a user by its Id
    public async Task<User> GetUserByIdAsync(int id)
    {
        return await _context.Users.FindAsync(id);
    }

    // Get all users
    public async Task<List<User>> GetAllUsersAsync()
    {
        return await _context.Users.ToListAsync();
    }
}
