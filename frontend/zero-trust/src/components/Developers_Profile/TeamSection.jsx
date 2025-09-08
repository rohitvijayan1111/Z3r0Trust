import { motion } from "framer-motion";
import { IconBrandGithub, IconBrandLinkedin } from "@tabler/icons-react";

const teamMembers = [
  {
    name: "Divakar G",
    role: "Team Leader",
    linkedin: "https://github.com/diva3501", // replace with actual
    github: "https://www.linkedin.com/in/divakar3501/", // replace with actual
  },
  {
    name: "Rohit Vijayan B",
    role: "Member",
    linkedin: "https://www.linkedin.com/in/rohitvijayan1111/",
    github: "https://github.com/rohitvijayan1111",
  },
  {
    name: "Kaviyarasu S",
    role: "Member",
    linkedin: "https://www.linkedin.com/in/kaviyarasu-sivaraj-312893262/",
    github: "https://github.com/kavirajmetech",
  },
  {
    name: "Rithik Raja S",
    role: "Member",
    linkedin: "https://www.linkedin.com/in/rithik-raja-s/",
    github: "https://github.com/RithikRaja28",
  },
  {
    name: "Gokul J",
    role: "Member",
    linkedin: "https://www.linkedin.com/in/gokul-jeyachandran-37a649229/",
    github: "https://github.com/GokulJeyachandran-1",
  },
];

export function TeamSection() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-900 to-black p-8">
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-white mb-12">
          👥 Meet Our Team
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          {teamMembers.map((member, idx) => (
            <motion.div
              key={idx}
              whileHover={{ scale: 1.05 }}
              className="bg-gradient-to-br from-zinc-800 to-zinc-900 rounded-2xl p-6 shadow-lg border border-zinc-700 hover:border-blue-500 transition"
            >
              <h3 className="text-xl font-semibold text-white">
                {member.name}
              </h3>
              <p className="text-zinc-400 mb-4">{member.role}</p>

              <div className="flex justify-center space-x-6 mt-4">
                <a
                  href={member.linkedin}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-500"
                >
                  <IconBrandLinkedin className="w-8 h-8" />
                </a>
                <a
                  href={member.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-gray-400"
                >
                  <IconBrandGithub className="w-8 h-8" />
                </a>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
