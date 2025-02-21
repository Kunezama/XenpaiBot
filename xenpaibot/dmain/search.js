import fs from 'fs';
import readline from 'readline';
import process from 'process';
import { execSync } from 'child_process';

async function installPackage(packageName) {
    try {
        await import(packageName);
        return true;
    } catch (error) {
        try {
            const { default: chalk } = await import('chalk');
            console.log(chalk.yellow(`You have not installed ${packageName}, it is being installed...`));
            execSync(`npm install ${packageName}`, { stdio: 'inherit' });
            console.log(chalk.green(`${packageName} installed successfully.`));
            return true;
        } catch (installError) {
            const { default: chalk } = await import('chalk');
            console.error(chalk.red(`Failed to install ${packageName}:`, installError.message));
            return false;
        }
    }
}

async function main() {
    let chalk;

    if (await installPackage('chalk')) {
        const { default: ch } = await import('chalk');
        chalk = ch;
    } else {
        console.error("Chalk installation failed. Exiting.");
        process.exit(1);
    }

    let axios;
    if (await installPackage('axios')) {
      const { default: ax } = await import('axios');
      axios = ax;
    } else {
        console.error("Axios installation failed. Exiting.");
        process.exit(1);
    }

    const clearScreen = () => {
        process.stdout.write('\x1Bc');
    };

    class DomainGrabber {
        constructor() {
            this.domains = new Set();
        }

        async searchDomains(keyword) {
            try {
                console.log(chalk.cyan(`\nSearching domains for keyword: ${keyword}`));
                const response = await axios.get(`https://website.informer.com/search.php?query=${keyword}`);

                const matches = response.data.match(/data-domain=\"(.*?)\"/g);
                if (matches) {
                    matches.forEach(match => {
                        const domain = match.match(/data-domain=\"(.*?)\"/)[1];
                        this.domains.add(domain);
                    });
                    console.log(chalk.green(`Found ${matches.length} domains for '${keyword}'.`));
                } else {
                    console.log(chalk.yellow(`No domains found for '${keyword}'.`));
                }
            } catch (error) {
                console.error(chalk.red(`Error fetching data for '${keyword}':`, error.message));
            }
        }

        async getUserInput() {
            const rl = readline.createInterface({
                input: process.stdin,
                output: process.stdout
            });

            return new Promise((resolve) => {
                rl.question(chalk.blue.bold(`Enter '${chalk.yellow('file')}' to input keywords from a file, or '${chalk.yellow('manual')}' for manual input: `), async (source) => {
                    if (source.trim().toLowerCase() === 'file') {
                        rl.question(chalk.magenta(`Enter the file path with keywords (one keyword per line): `), (filePath) => {
                            const validatedPath = this.validateFilePath(filePath);
                            if (validatedPath) {
                                try {
                                    const data = fs.readFileSync(validatedPath, 'utf-8');
                                    const keywords = data.split('\n').map(line => line.trim()).filter(line => line);
                                    console.log(chalk.green(`Loaded ${keywords.length} keywords from file.`));
                                    rl.close();
                                    resolve(keywords);
                                } catch (error) {
                                    console.error(chalk.red(`Error: File not found or cannot be read. Please check the file path.`));
                                    rl.close();
                                    resolve([]);
                                }
                            } else {
                                console.error(chalk.red(`Error: File path is invalid or file not found.`));
                                rl.close();
                                resolve([]);
                            }
                        });
                    } else if (source.trim().toLowerCase() === 'manual') {
                        rl.question(chalk.cyan(`Enter the number of keywords: `), (numKeywords) => {
                            let keywords = [];
                            const askKeyword = (index) => {
                                if (index < parseInt(numKeywords)) {
                                    rl.question(chalk.yellow(`Enter keyword ${index + 1}: `), (keyword) => {
                                        if (keyword.trim()) {
                                            keywords.push(keyword.trim());
                                        }
                                        askKeyword(index + 1);
                                    });
                                } else {
                                    console.log(chalk.green(`Added ${keywords.length} keywords manually.`));
                                    rl.close();
                                    resolve(keywords);
                                }
                            };
                            askKeyword(0);
                        });
                    } else {
                        console.log(chalk.red(`Invalid input. Please enter 'file' or 'manual'.`));
                        rl.close();
                        resolve([]);
                    }
                });
            });
        }

        validateFilePath(filePath) {
            try {
                fs.accessSync(filePath, fs.constants.R_OK);
                return filePath;
            } catch (error) {
                return null;
            }
        }

        async saveDomainsToFile() {
            const rl = readline.createInterface({
                input: process.stdin,
                output: process.stdout
            });

            return new Promise((resolve) => {
                rl.question(chalk.cyan(`Enter the file name to save domains (default: Results-Domains.txt): `), (fileName) => {
                    const finalFileName = fileName.trim() || 'Results-Domains.txt';
                    try {
                        fs.writeFileSync(finalFileName, Array.from(this.domains).join('\n'));
                        console.log(chalk.green(`\n${this.domains.size} domains saved to '${finalFileName}' successfully.`));
                    } catch (error) {
                        console.error(chalk.red(`An unexpected error occurred while saving to file:`, error.message));
                    } finally {
                        rl.close();
                        resolve();
                    }
                });
            });
        }

        printDomains() {
            if (this.domains.size > 0) {
                console.log(chalk.blue(`\nFound domains:`));
                this.domains.forEach(domain => console.log(domain));
            } else {
                console.log(chalk.yellow(`\nNo domains found.`));
            }
        }

        async run() {
            clearScreen();
            const asciiArt = `
${chalk.cyan.bold(' ____  ____   __   ____   ___  _  _ ')}
${chalk.cyan.bold('/ ___)(  __) / _\\ (  _ \\ / __)/ )( \\')}
${chalk.cyan.bold('\\___ \\ ) _) /    \\ )   /( (__ ) __ ( ')}
${chalk.cyan.bold('(____/(____)\\_/\\_/(__\\_) \\___)\\_)(_/' )}
${chalk.reset()}
${chalk.yellow.bold('Author : Kanezama')}
`; 

            console.log(asciiArt);
            console.log(chalk.magenta.bold(`\nXenpaiBot - Domain Grabber for Pentesters\n`)); // Kurung penutup ditambahkan

            const keywords = await this.getUserInput();

            if (keywords.length > 0) {
                console.log(chalk.blue(`Starting domain search...`));
                let i = 0;
                for (const keyword of keywords) {
                    i++;
                    console.log(chalk.yellow(`Searching ${i} of ${keywords.length} keywords...`));
                    await this.searchDomains(keyword);
                }
                await this.saveDomainsToFile();
                this.printDomains();
            } else {
                console.log(chalk.red(`No keywords provided. Exiting...`));
            }
        }
    }

    const grabber = new DomainGrabber();
    await grabber.run();
}

main();
