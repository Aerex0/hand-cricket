import mediapipe as mp
import cv2 as cv
import random
import imageio
import os
import pygame
import tkinter as tk


def load_sounds():
    """Load all game sound effects"""
    pygame.mixer.init()
    
    sounds = {}
    sound_files = {
        'out': "assets/out.wav",
        'run': "assets/score.wav", 
        'win': "assets/Win.wav",
        'lose': "assets/lose.wav",
        'tie': "assets/tie.wav"
    }
    
    for sound_name, file_path in sound_files.items():
        try:
            sounds[sound_name] = pygame.mixer.Sound(file_path)
        except Exception as e:
            print(f"Error loading {sound_name} sound: {e}")
            sounds[sound_name] = None
    
    return sounds


def load_gif_frames(gif_path, gif_name):
    """Load and process GIF frames for animations"""
    try:
        gif_data = imageio.mimread(gif_path)
        frames = []
        for frame in gif_data:
            if frame.shape[2] == 4:  # Has alpha channel
                frames.append(cv.cvtColor(frame, cv.COLOR_RGBA2BGRA))
            else:  # RGB only
                frames.append(cv.cvtColor(frame, cv.COLOR_RGB2BGR))
        return frames
    except Exception as e:
        print(f"Error loading {gif_name} gif: {e}")
        return []


def load_animations():
    """Load all game animations"""
    animations = {}
    
    gif_files = {
        'victory': "assets/Victory.gif",
        'game_over': "assets/game-over-game.gif"
    }
    
    for anim_name, file_path in gif_files.items():
        animations[anim_name] = load_gif_frames(file_path, anim_name)
    
    return animations


def get_screen_dimensions():
    """Get screen resolution for fullscreen display"""
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def get_hand_run(hand_landmarks):
    """Improved finger counting while maintaining original logic structure"""
    lm = hand_landmarks.landmark

    # Finger tip and pip landmarks for better accuracy
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    pip_ids = [2, 6, 10, 14, 18]  # Corresponding PIP joints

    fingers = []

    # Thumb (special case - check x coordinate)
    if (lm[tip_ids[0]].y < lm[pip_ids[0]].y and 
        lm[tip_ids[0]].y < lm[tip_ids[1]].y and 
        lm[tip_ids[0]].y < lm[tip_ids[2]].y and 
        lm[tip_ids[0]].y < lm[tip_ids[3]].y):
        fingers.append(6)
    else:
        fingers.append(0)
    
    # Other fingers (check y coordinate)
    for i in range(1, 5):
        if lm[tip_ids[i]].y < lm[pip_ids[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    finger_count = sum(fingers)
    
    # Map to 1-6 range (if 0 fingers, return 1)
    return max(1, min(6, finger_count))


def apply_gif_overlay(frame, gif_frame, screen_width, screen_height, alpha=0.7):
    """Apply GIF frame overlay to the main frame"""
    gif_frame = cv.resize(gif_frame, (screen_width, screen_height))
    
    # Check if frame has alpha channel
    if gif_frame.shape[2] == 4:
        b, g, r, a = cv.split(gif_frame)
        overlay_rgb = cv.merge((b, g, r))
        alpha_mask = a / 255.0
        for c in range(3):
            frame[:, :, c] = (alpha_mask * overlay_rgb[:, :, c] +
                              (1 - alpha_mask) * frame[:, :, c])
    else:
        # Simple overlay without alpha blending
        frame = cv.addWeighted(frame, 0.3, gif_frame, alpha, 0)
    
    return frame


def draw_game_ui(frame, clock, gameresult, gametext, player_score, computer_score, 
                round_num, innings, screen_width, screen_height, is_out):
    """Draw all game UI elements"""
    # Game title at top center
    title_text = "HAND CRICKET"
    title_size = cv.getTextSize(title_text, cv.FONT_HERSHEY_DUPLEX, 4, 4)[0]
    title_x = (screen_width - title_size[0]) // 2
    cv.putText(frame, title_text, (title_x, 120), cv.FONT_HERSHEY_DUPLEX, 4, (200, 255, 200), 4)
    
    cv.putText(frame, f"clock : {clock}", (50, 180), cv.FONT_HERSHEY_PLAIN, 3, (200, 255, 200), 3)
    cv.putText(frame, gameresult, (50, 230), cv.FONT_HERSHEY_PLAIN, 3, (200, 255, 200), 3)
    cv.putText(frame, gametext, (50, 280), cv.FONT_HERSHEY_PLAIN, 3, (200, 255, 200), 3)
    cv.putText(frame, f"You: {player_score} | Computer: {computer_score}", 
               (50, 330), cv.FONT_HERSHEY_PLAIN, 3, (200, 255, 200), 3)
    
    # Round and Innings text with proper spacing from right edge
    round_innings_text = f"Round: {round_num} | Innings: {innings}"
    round_innings_size = cv.getTextSize(round_innings_text, cv.FONT_HERSHEY_PLAIN, 3, 3)[0]
    round_innings_x = screen_width - round_innings_size[0] - 50
    cv.putText(frame, round_innings_text, (round_innings_x, 180), 
               cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    # Bottom instruction bar
    cv.rectangle(frame, (int(screen_width*0.3), int(screen_height*0.85)), 
                 (int(screen_width*0.7), int(screen_height*0.95)), (200, 255, 200), -1)
    
    if innings == 2 and is_out:
        cv.putText(frame, "Press 'N' to Restart Game", 
                   (int(screen_width*0.32), int(screen_height*0.91)), 
                   cv.FONT_HERSHEY_SIMPLEX, 1.2, (200, 255, 200), 3)
    else:
        cv.putText(frame, "Auto Next Round", 
                   (int(screen_width*0.4), int(screen_height*0.91)), 
                   cv.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)


def play_hand_cricket():
    """Main game function"""
    # Load resources
    sounds = load_sounds()
    animations = load_animations()
    screen_width, screen_height = get_screen_dimensions()
    
    # Setup audio channels
    run_channel = pygame.mixer.Channel(1)
    event_channel = pygame.mixer.Channel(2)
    
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    
    # Video setup
    vid = cv.VideoCapture(0)
    vid.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    vid.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    # Create fullscreen window
    cv.namedWindow('frame', cv.WINDOW_NORMAL)
    cv.setWindowProperty('frame', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    
    # Game state variables
    clock = 0
    player_move = None
    computer_move = None
    gametext = "Press 'S' to Start the Game!"
    success = True
    gameresult = ""
    player_score = 0
    computer_score = 0
    scored_this_round = False
    is_player_batting = True
    is_out = False
    innings = 1
    round_num = 0
    game_started = False
    celebration_frame_idx = 0
    celebrating_win = False
    celebrating_lose = False
    gif_played_win = False
    gif_played_lose = False
    run_sound_playing = False
    
    with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, 
                        min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = vid.read()
            if not ret:
                break

            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = hands.process(frame)
            frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
            frame = cv.flip(frame, 1)
            
            # Resize frame to fill screen
            frame = cv.resize(frame, (screen_width, screen_height))

            # Check for animation triggers
            if "You Won the Game!" in gametext and not celebrating_win and not gif_played_win:
                celebrating_win = True
                celebration_frame_idx = 0
            elif "You Lost the Game!" in gametext and not celebrating_lose and not gif_played_lose:
                celebrating_lose = True
                celebration_frame_idx = 0

            # WINNING CELEBRATION
            if celebrating_win and not gif_played_win and animations['victory']:
                if celebration_frame_idx < len(animations['victory']):
                    frame = apply_gif_overlay(frame, animations['victory'][celebration_frame_idx], 
                                            screen_width, screen_height)
                    celebration_frame_idx += 1
                else:
                    gif_played_win = True
                    celebrating_win = False

            # LOSING CELEBRATION
            if celebrating_lose and not gif_played_lose and animations['game_over']:
                if celebration_frame_idx < len(animations['game_over']):
                    frame = apply_gif_overlay(frame, animations['game_over'][celebration_frame_idx], 
                                            screen_width, screen_height)
                    celebration_frame_idx += 1
                else:
                    gif_played_lose = True
                    celebrating_lose = False

            # Game logic
            if clock == 0:
                if game_started:
                    round_num += 1
                    scored_this_round = False
                    gameresult = ""

            # Sound management - Play run sound during active gameplay
            if game_started and 10 <= clock <= 30 and not run_sound_playing:
                if sounds['run']:
                    run_channel.play(sounds['run'], loops=-1)
                run_sound_playing = True
            elif (clock < 10 or clock > 30) and run_sound_playing:
                run_channel.stop()
                run_sound_playing = False

            if not game_started:
                gametext = "Press 'S' to Start the Game!"
            elif 0 <= clock < 5:
                success = True
                gametext = "Get Ready..."
            elif 5 <= clock < 15:
                gametext = "Show your hand!"
            elif clock == 15:
                hls = results.multi_hand_landmarks
                if hls and len(hls) > 0:
                    player_move = get_hand_run(hls[0])
                    computer_move = random.choice([1, 2, 3, 4, 6])
                else:
                    success = False

            elif 15 < clock < 25:
                if success:
                    gameresult = f"You: {player_move}  |  Computer: {computer_move}"

                    if not scored_this_round:
                        if player_move == computer_move:
                            gametext = f"OUT!"
                            is_out = True
                            # Player is OUT - stop run sound
                            if run_sound_playing:
                                run_channel.stop()
                                run_sound_playing = False
                            if sounds['out']:
                                event_channel.play(sounds['out'])
                        else:
                            run = player_move if is_player_batting else computer_move
                            if is_player_batting:
                                player_score += run
                                gametext = f"You scored {run} run(s)"
                            else:
                                computer_score += run
                                gametext = f"Computer scored {run} run(s)"
                                # Check if computer wins during their batting
                                if innings == 2 and computer_score > player_score:
                                    gametext = "Computer Won! They chased the target!"
                                    is_out = True
                        scored_this_round = True
                else:
                    gametext = "Hand not detected!"

            elif clock == 25:
                if is_out:
                    if innings == 1:
                        is_player_batting = False
                        is_out = False
                        gametext = "Innings Over. Now Computer Bats!"
                        innings += 1
                    else:
                        # Stop run sound at game end
                        if run_sound_playing:
                            run_channel.stop()
                            run_sound_playing = False
                            
                        if player_score > computer_score:
                            gametext = "You Won the Game! Press 'n' to restart"
                            if sounds['win']:
                                event_channel.play(sounds['win'])
                        elif computer_score > player_score:
                            gametext = "You Lost the Game! Press 'n' to restart"
                            if sounds['lose']:
                                event_channel.play(sounds['lose'])
                        else:
                            gametext = "It's a Tie! Press 'n' to restart"
                            if sounds['tie']:
                                event_channel.play(sounds['tie'])
                                
            elif clock > 25:
                # Auto-restart immediately for next round if not game over
                if not (innings == 2 and is_out):  # If game is not over
                    clock = -1  # Will become 0 after increment
                    gametext = ""
                    gameresult = ""
                    player_move = None
                    computer_move = None
                    success = True

            # Draw game UI
            draw_game_ui(frame, clock, gameresult, gametext, player_score, computer_score, 
                        round_num, innings, screen_width, screen_height, is_out)
            
            cv.imshow('frame', frame)

            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s') and not game_started:  # Start the game
                game_started = True
                clock = 0
                gametext = ""
            elif key == ord('n') and (innings == 2 and is_out):  # Only need 'n' to restart after game over
                player_score = 0
                computer_score = 0
                is_player_batting = True
                innings = 1
                round_num = 0
                clock = 0
                gametext = ""
                gameresult = ""
                player_move = None
                computer_move = None
                is_out = False
                success = True
                scored_this_round = False
                game_started = False
                
                # Reset animation flags
                gif_played_win = False
                gif_played_lose = False
                celebrating_win = False
                celebrating_lose = False
                celebration_frame_idx = 0
                
                # Stop all sounds
                run_channel.stop()
                event_channel.stop()
                run_sound_playing = False

            if game_started and (clock <= 50 or (clock > 50 and not (innings == 2 and is_out))):
                clock += 1

    vid.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    play_hand_cricket()