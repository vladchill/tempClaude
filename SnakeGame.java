import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.LinkedList;
import java.util.Random;

public class SnakeGame extends JPanel implements ActionListener, KeyListener {
    private static final int WIDTH = 600;
    private static final int HEIGHT = 600;
    private static final int CELL = 20;
    private static final int COLS = WIDTH / CELL;
    private static final int ROWS = HEIGHT / CELL;
    private static final int DELAY = 120;

    private LinkedList<Point> snake;
    private Point food;
    private int dx, dy;
    private boolean running;
    private boolean gameOver;
    private int score;
    private Timer timer;
    private Random random = new Random();

    public SnakeGame() {
        setPreferredSize(new Dimension(WIDTH, HEIGHT));
        setBackground(Color.BLACK);
        setFocusable(true);
        addKeyListener(this);
        initGame();
    }

    private void initGame() {
        snake = new LinkedList<>();
        snake.add(new Point(COLS / 2, ROWS / 2));
        snake.add(new Point(COLS / 2 - 1, ROWS / 2));
        snake.add(new Point(COLS / 2 - 2, ROWS / 2));
        dx = 1;
        dy = 0;
        score = 0;
        running = true;
        gameOver = false;
        spawnFood();
        if (timer != null) timer.stop();
        timer = new Timer(DELAY, this);
        timer.start();
    }

    private void spawnFood() {
        Point p;
        do {
            p = new Point(random.nextInt(COLS), random.nextInt(ROWS));
        } while (snake.contains(p));
        food = p;
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (!running) return;

        Point head = snake.getFirst();
        Point newHead = new Point(head.x + dx, head.y + dy);

        if (newHead.x < 0 || newHead.x >= COLS || newHead.y < 0 || newHead.y >= ROWS
                || snake.contains(newHead)) {
            running = false;
            gameOver = true;
            timer.stop();
            repaint();
            return;
        }

        snake.addFirst(newHead);
        if (newHead.equals(food)) {
            score++;
            spawnFood();
        } else {
            snake.removeLast();
        }
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;

        // Draw grid (subtle)
        g2.setColor(new Color(30, 30, 30));
        for (int x = 0; x < WIDTH; x += CELL) g2.drawLine(x, 0, x, HEIGHT);
        for (int y = 0; y < HEIGHT; y += CELL) g2.drawLine(0, y, WIDTH, y);

        // Draw food
        g2.setColor(Color.RED);
        g2.fillOval(food.x * CELL + 2, food.y * CELL + 2, CELL - 4, CELL - 4);

        // Draw snake
        for (int i = 0; i < snake.size(); i++) {
            Point p = snake.get(i);
            g2.setColor(i == 0 ? new Color(0, 220, 0) : new Color(0, 160, 0));
            g2.fillRoundRect(p.x * CELL + 1, p.y * CELL + 1, CELL - 2, CELL - 2, 6, 6);
        }

        // Draw score
        g2.setColor(Color.WHITE);
        g2.setFont(new Font("Arial", Font.BOLD, 16));
        g2.drawString("Score: " + score, 10, 20);

        // Draw game over
        if (gameOver) {
            g2.setColor(new Color(0, 0, 0, 160));
            g2.fillRect(0, 0, WIDTH, HEIGHT);
            g2.setColor(Color.WHITE);
            g2.setFont(new Font("Arial", Font.BOLD, 36));
            String msg = "GAME OVER";
            FontMetrics fm = g2.getFontMetrics();
            g2.drawString(msg, (WIDTH - fm.stringWidth(msg)) / 2, HEIGHT / 2 - 20);
            g2.setFont(new Font("Arial", Font.PLAIN, 18));
            String sub = "Score: " + score + "  |  Press R to restart";
            fm = g2.getFontMetrics();
            g2.drawString(sub, (WIDTH - fm.stringWidth(sub)) / 2, HEIGHT / 2 + 20);
        }
    }

    @Override
    public void keyPressed(KeyEvent e) {
        switch (e.getKeyCode()) {
            case KeyEvent.VK_UP:    if (dy == 0) { dx = 0; dy = -1; } break;
            case KeyEvent.VK_DOWN:  if (dy == 0) { dx = 0; dy = 1;  } break;
            case KeyEvent.VK_LEFT:  if (dx == 0) { dx = -1; dy = 0; } break;
            case KeyEvent.VK_RIGHT: if (dx == 0) { dx = 1; dy = 0;  } break;
            case KeyEvent.VK_R:     if (gameOver) initGame(); break;
        }
    }

    @Override public void keyReleased(KeyEvent e) {}
    @Override public void keyTyped(KeyEvent e) {}

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Snake");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.add(new SnakeGame());
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setResizable(false);
            frame.setVisible(true);
        });
    }
}
