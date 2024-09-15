using AppServer.Models;
using Microsoft.AspNetCore.Mvc;

[Route("api/user")]
[ApiController]
public class UserController : ControllerBase
{
    private readonly IUserService _userService;

    public UserController(IUserService userService)
    {
        _userService = userService;
    }

    // POST: api/user/add
    [HttpPost("add")]
    public async Task<IActionResult> PostUser([FromBody] User user)
    {
        await _userService.AddUserAsync(user);
        return Ok("User successfully added");
    }

    // DELETE: api/user/delete/{id}
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        await _userService.DeleteUserAsync(id);
        return Ok("User successfully deleted");
    }

    // DELETE: api/user/delete/all
    [HttpDelete("delete/all")]
    public async Task<IActionResult> DeleteAllUsers()
    {
        await _userService.DeleteAllUsersAsync();
        return Ok("All users deleted successfully.");
    }


    // GET: api/user/get/{id}
    [HttpGet("get/{id}")]
    public async Task<IActionResult> GetUserById(int id)
    {
        var user = await _userService.GetUserByIdAsync(id);
        if (user == null)
        {
            return NotFound();
        }
        return Ok(user);
    }

    // GET: api/user
    [HttpGet("get/all")]
    public async Task<IActionResult> GetAllUsers()
    {
        var users = await _userService.GetAllUsersAsync();
        return Ok(users);
    }
}
